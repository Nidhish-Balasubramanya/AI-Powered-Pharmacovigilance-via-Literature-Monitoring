import os
import json
import uuid
import boto3
import tempfile
from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse
from fastapi import Request

from literature_ingestion.text_extraction import handle_file
from aer_entity_extraction.ner_pipeline import extract_entities
from case_data_construction.json_generator import build_case_json
from narrative_generation.narrative_generator import generate_narrative
from narrative_generation.prompt_builder import build_prompt_from_json

# --- AWS S3 Setup ---
AWS_REGION = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
S3_BUCKET = os.environ.get("S3_BUCKET", "your_bucket_name")
s3 = boto3.client("s3", region_name=AWS_REGION)

app = FastAPI(title="AI-Powered Pharmacovigilance API")


class LimitUploadSizeMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_upload_size: int):
        super().__init__(app)
        self.max_upload_size = max_upload_size  # bytes

    async def dispatch(self, request: Request, call_next):
        content_length = request.headers.get("content-length")
        if content_length and int(content_length) > self.max_upload_size:
            return JSONResponse(
                status_code=413,
                content={"detail": "File too large. Max allowed size is 20 MB."}
            )
        return await call_next(request)

app.add_middleware(LimitUploadSizeMiddleware, max_upload_size=20 * 1024 * 1024)  # 20MB


origins = [
    "http://localhost",
    "http://localhost:8501",
    "http://127.0.0.1",
    "http://127.0.0.1:8501",
    "*"  # Allow all origins for testing; restrict in production
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- S3 Helper Functions ---
def s3_upload_bytes(data_bytes, key, content_type):
    s3.put_object(Bucket=S3_BUCKET, Key=key, Body=data_bytes, ContentType=content_type)

def s3_upload_json(data, key):
    s3.put_object(Bucket=S3_BUCKET, Key=key, Body=json.dumps(data), ContentType="application/json")

def s3_download_bytes(key):
    try:
        obj = s3.get_object(Bucket=S3_BUCKET, Key=key)
        return obj['Body'].read()
    except s3.exceptions.NoSuchKey:
        return None

def s3_download_json(key):
    data = s3_download_bytes(key)
    if data is None:
        return None
    return json.loads(data.decode('utf-8'))

def s3_key_exists(key):
    try:
        s3.head_object(Bucket=S3_BUCKET, Key=key)
        return True
    except s3.exceptions.ClientError:
        return False

# --- API Endpoints ---

@app.post("/upload")
async def upload_literature(file: UploadFile = File(...)):
    case_id = uuid.uuid4().hex
    filename = file.filename.lower()
    s3_upload_key = f"uploads/{case_id}_{filename}"

    file_bytes = await file.read()
    s3_upload_bytes(file_bytes, s3_upload_key, file.content_type or "application/octet-stream")

    # Detect type
    if filename.endswith(".pdf"):
        file_type = "pdf"
    elif filename.endswith(".txt"):
        file_type = "txt"
    elif filename.endswith((".jpg", ".jpeg", ".png")):
        file_type = "image"
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type.")

    # Save temp file
    temp_dir = tempfile.gettempdir()
    tmp_path = os.path.join(temp_dir, f"{case_id}_{filename}")
    with open(tmp_path, "wb") as f:
        f.write(file_bytes)

    try:
        extracted_text = handle_file(tmp_path, file_type)
        entities = extract_entities(extracted_text)
        case_json = build_case_json(entities)
        case_key = f"cases/vault_{case_id}.json"
        s3_upload_json(case_json, case_key)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

    return {
        "case_id": case_id,
        "message": "Case data extracted successfully.",
        "case_json": case_json
    }


@app.get("/case/{case_id}")
async def get_case(case_id: str):
    case_key = f"cases/vault_{case_id}.json"
    case_json = s3_download_json(case_key)
    if case_json is None:
        raise HTTPException(status_code=404, detail="Case not found.")
    return case_json

@app.post("/narrative")
async def generate_case_narrative(case_id: str):
    case_key = f"cases/vault_{case_id}.json"
    case_json = s3_download_json(case_key)
    if case_json is None:
        raise HTTPException(status_code=404, detail="Case not found.")

    prompt = build_prompt_from_json(case_json)
    narrative = generate_narrative(prompt)
    narrative_key = f"narratives/narrative_{case_id}.txt"
    s3_upload_bytes(narrative.encode("utf-8"), narrative_key, "text/plain")
    return {
        "case_id": case_id,
        "narrative": narrative
    }

@app.get("/download/case/{case_id}")
async def download_case_json(case_id: str):
    case_key = f"cases/vault_{case_id}.json"
    data = s3_download_bytes(case_key)
    if data is None:
        raise HTTPException(status_code=404, detail="Case not found.")
    return StreamingResponse(
        iter([data]),
        media_type="application/json",
        headers={"Content-Disposition": f"attachment; filename=case_{case_id}.json"}
    )

@app.get("/download/narrative/{case_id}")
async def download_narrative_txt(case_id: str):
    narrative_key = f"narratives/narrative_{case_id}.txt"
    data = s3_download_bytes(narrative_key)
    if data is None:
        raise HTTPException(status_code=404, detail="Narrative not found.")
    return StreamingResponse(
        iter([data]),
        media_type="text/plain",
        headers={"Content-Disposition": f"attachment; filename=narrative_{case_id}.txt"}
    )

@app.post("/validate")
async def validate_case(case_id: str = Form(...), feedback: str = Form(...)):
    feedback_key = f"feedbacks/feedback_{case_id}.txt"
    s3_upload_bytes(feedback.encode("utf-8"), feedback_key, "text/plain")
    return {"message": "Feedback received. Thank you!"}

@app.get("/health")
def health():
    return {"status": "ok"}

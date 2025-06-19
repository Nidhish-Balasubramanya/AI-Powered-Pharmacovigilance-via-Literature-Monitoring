
# AI-Powered Pharmacovigilance via Literature Monitoring
<br>
This repository contains the full implementation of an **AI-powered pharmacovigilance system** that automates the extraction of **Adverse Event Reports (AERs)** and generates detailed **narrative case reports** from unstructured pharmaceutical literature.

The system combines traditional NLP, biomedical entity extraction, LLM-based summarization, and full-stack deployment components, providing a complete solution for regulatory safety reporting.
<br>
## Features

- **Literature Ingestion:** Handles pharmaceutical documents (PDF/HTML) and extracts clean text using OCR and parsing.
- **AER Entity Extraction:** Extracts structured data like drug name, dosage, reaction, etc., using BioBERT/SciSpacy + rule-based pipelines.
- **Vault-compliant JSON Generation:** Formats data into standard regulatory JSON schema for downstream use.
- **Narrative Generation:** Uses Claude Sonnet (via AWS Bedrock) to generate fluent case narratives from structured AER data.
- **REST API Backend:** Exposes core functionalities through a FastAPI server with endpoints for file upload, JSON output, and feedback submission.
- **Streamlit Frontend:** Interactive interface for uploading literature and viewing extracted reports in real time.
- **Containerized Deployment:** Deployed with Docker, NGINX (HTTPS), and AWS EC2.
<br>

## Folder Structure

```
pharmacovigilance/
├── aer_entity_extraction/
│   ├── __pycache__/
│   ├── __init__.py
│   ├── ner_pipeline.py
│   ├── rule_extractors.py
│   └── testrun.py
│
├── case_data_construction/
│   ├── __pycache__/
│   ├── __init__.py
│   ├── json_generator.py
│   └── testrun2.py
│
├── literature_ingestion/
│   ├── __pycache__/
│   ├── __init__.py
│   └── text_extraction.py
│
├── narrative_generation/
│   ├── __pycache__/
│   ├── __init__.py
│   ├── narrative_generator.py
│   └── prompt_builder.py
│
├── nginx/
│   ├── certs/
│   ├── Dockerfile
│   └── nginx.conf
│
├── rest_api/
│   ├── __pycache__/
│   ├── __init__.py
│   ├── .dockerignore
│   ├── Dockerfile
│   ├── main.py
│   └── requirements.txt
│
├── streamlit/
│   ├── .dockerignore
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── docker-compose.yml
└── requirements.txt

```

## Setup & Deployment

### 1. Clone the Repository

```bash
git clone https://github.com/Nidhish-Balasubramanya/AI-Powered-Pharmacovigilance-via-Literature-Monitoring
cd pharmacovigilance-app
```

### 2. Local Development

- Python 3.10+
- Create virtual env:

```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

### 3. Run via Docker Compose

```bash
docker-compose up --build
```

This starts:
- REST API backend on `http://localhost:8000`
- Streamlit frontend on `http://localhost:8501`
- HTTPS via NGINX reverse proxy (certificates must be configured)

<br>


## REST API Endpoints (FastAPI)

### 1 `POST /upload`

**Description:** Upload a pharmaceutical document (`.pdf`, `.txt`, or image) to extract AER entities and construct a Vault-compatible JSON.

* **Request:** `multipart/form-data`

  * `file`: The literature document to upload

* **Response:**

```json
{
  "case_id": "a1b2c3d4...",
  "message": "Case data extracted successfully.",
  "case_json": { }
}
```

* **Errors:** `400` (Unsupported file type), `500` (Processing failed)



### 2 `GET /case/{case_id}`

**Description:** Fetch the JSON-structured AER case generated from the uploaded literature.

* **Path Param:** `case_id` – Unique ID of the case
* **Response:** JSON content of the AER case
* **Errors:** `404` if not found



### 3 `POST /narrative`

**Description:** Generate a narrative from a previously extracted case.

* **Query Param:** `case_id`

* **Response:**

```json
{
  "case_id": "a1b2c3d4...",
  "narrative": "Patient experienced..."
}
```

* **Errors:** `404` if case not found



### 4 `GET /download/case/{case_id}`

**Description:** Download the structured AER JSON file.

* **Path Param:** `case_id`
* **Response:** Attachment (`.json`) as `application/json`
* **Errors:** `404` if case not found



### 5 `GET /download/narrative/{case_id}`

**Description:** Download the generated narrative as a `.txt` file.

* **Path Param:** `case_id`
* **Response:** Attachment (`.txt`) as `text/plain`
* **Errors:** `404` if narrative not found



### 6 `POST /validate`

**Description:** Submit validation feedback for a specific case.

* **Form Params:**

  * `case_id`: ID of the case being reviewed
  * `feedback`: Free-text feedback message

* **Response:**

```json
{
  "message": "Feedback received. Thank you!"
}
```



### 7 `GET /health`

**Description:** Simple health check for uptime and monitoring.

* **Response:**

```json
{
  "status": "ok"
}
```
<br>

## Frontend (Streamlit)

The Streamlit UI allows:
- Uploading documents
- Viewing extracted JSON
- Triggering narrative generation
- Displaying full case report

Accessible via: `https://pharmacovigilence.com/`
<br>
## Tech Stack

- Python 3.10, FastAPI, Streamlit
- SciSpacy, BioBERT/ClinicalBERT, AWS Bedrock (Claude)
- Docker, NGINX, AWS EC2
- Vault JSON Schema, OCR, Regex/Ruled NER

## License

This work is licensed under CC BY-NC-ND 4.0.
<br>
## Contact

For queries or feedback, feel free to open an issue or contact via the official project portal at [https://pharmacovigilence.com](https://pharmacovigilence.com)

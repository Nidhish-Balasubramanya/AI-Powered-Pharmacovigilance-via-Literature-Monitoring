import boto3
import json
from .prompt_builder import build_prompt_from_json

s3 = boto3.client("s3")
BUCKET_NAME = "<your_bucket_name" 

def generate_narrative(prompt):
    client = boto3.client("bedrock-runtime", region_name="us-east-1")
    body = json.dumps({
        "prompt": f"\n\nHuman: {prompt}\n\nAssistant:",
        "max_tokens_to_sample": 1024,
        "temperature": 0.7,
        "stop_sequences": ["\n\nHuman:"]
    })
    response = client.invoke_model(
        body=body,
        modelId="anthropic.claude-v2",
        accept="application/json",
        contentType="application/json"
    )
    response_body = json.loads(response['body'].read())
    return response_body.get('completion', '[No narrative returned]')


def load_json_from_s3(case_id):
    key = f"cases/{case_id}.json"  # adjust path if needed
    response = s3.get_object(Bucket=BUCKET_NAME, Key=key)
    data = json.loads(response['Body'].read().decode("utf-8"))
    return data, key


def save_json_to_s3(data, key):
    s3.put_object(
        Bucket=BUCKET_NAME,
        Key=key,
        Body=json.dumps(data, indent=2).encode("utf-8"),
        ContentType="application/json"
    )


# === MAIN EXECUTION ===
def run(case_id):
    try:
        # 1. Load JSON from S3
        data, s3_key = load_json_from_s3(case_id)

        # 2. Build prompt from full JSON
        prompt = build_prompt_from_json(data)

        # 3. Generate narrative
        narrative = generate_narrative(prompt)
        print("\nGenerated Narrative:\n", narrative)

        # 4. Inject narrative into JSON
        data["data"]["detail"]["structured"]["narrative__v"] = narrative

        # 5. Save it back to same S3 key
        save_json_to_s3(data, s3_key)
        print(f"✅ Updated JSON saved to S3: s3://{BUCKET_NAME}/{s3_key}")

    except Exception as e:
        print(f"❌ Error: {str(e)}")

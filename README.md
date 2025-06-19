
# AI-Powered Pharmacovigilance via Literature Monitoring

This repository contains the full implementation of an **AI-powered pharmacovigilance system** that automates the extraction of **Adverse Event Reports (AERs)** and generates detailed **narrative case reports** from unstructured pharmaceutical literature.

The system combines traditional NLP, biomedical entity extraction, LLM-based summarization, and full-stack deployment components, providing a complete solution for regulatory safety reporting.

## Features

- **Literature Ingestion:** Handles pharmaceutical documents (PDF/HTML) and extracts clean text using OCR and parsing.
- **AER Entity Extraction:** Extracts structured data like drug name, dosage, reaction, etc., using BioBERT/SciSpacy + rule-based pipelines.
- **Vault-compliant JSON Generation:** Formats data into standard regulatory JSON schema for downstream use.
- **Narrative Generation:** Uses Claude Sonnet (via AWS Bedrock) to generate fluent case narratives from structured AER data.
- **REST API Backend:** Exposes core functionalities through a FastAPI server with endpoints for file upload, JSON output, and feedback submission.
- **Streamlit Frontend:** Interactive interface for uploading literature and viewing extracted reports in real time.
- **Containerized Deployment:** Deployed with Docker, NGINX (HTTPS), and AWS EC2.

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

## REST API Endpoints (FastAPI)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST   | `/upload/` | Uploads pharmaceutical document |
| GET    | `/get_json/{case_id}` | Retrieves extracted Vault JSON |
| POST   | `/generate_narrative/` | Triggers Claude-based narrative generation |
| POST   | `/feedback/` | Accepts user feedback on generated output |

## Frontend (Streamlit)

The Streamlit UI allows:
- Uploading documents
- Viewing extracted JSON
- Triggering narrative generation
- Displaying full case report

Accessible via: `https://pharmacovigilence.com/`

## Tech Stack

- Python 3.10, FastAPI, Streamlit
- SciSpacy, BioBERT/ClinicalBERT, AWS Bedrock (Claude)
- Docker, NGINX, AWS EC2
- Vault JSON Schema, OCR, Regex/Ruled NER


## License

This work is licensed under CC BY-NC-ND 4.0.

## Contact

For queries or feedback, feel free to open an issue or contact via the official project portal at [https://pharmacovigilence.com](https://pharmacovigilence.com)

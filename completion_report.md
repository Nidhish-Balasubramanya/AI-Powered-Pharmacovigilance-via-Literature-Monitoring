# Completion Report – AI-Powered Pharmacovigilance via Literature Monitoring


---

## 1. Literature Ingestion

**Requirement:**  
Extract full text from pharmaceutical literature PDFs, HTMLs, and text files.

**Implementation:**  
- Module: `1_literature_ingestion/text_extraction.py`
- Supports `.pdf`, `.png/.jpg/.jpeg`, `.txt`
- Handles noisy formatting using heuristic and layout-based rules

---

## 2. AER Entity Extraction

**Requirement:**  
Extract structured Adverse Event Report (AER) fields: Drug, Event, Indication, Dosage, Route, Patient Info, Reporter Info.

**Implementation:**  
- Module: `2_aer_entity_extraction/ner_pipeline.py`
- Combines: `SciSpacy + BioBERT` NER with custom rule-based post-processing
- Final output standardized to Vault-compatible schema

---

## 3. Case Data Construction

**Requirement:**  
Convert extracted entities into Vault-style JSON case files.

**Implementation:**  
- Module: `3_case_data_construction/json_generator.py`
- Produces validated, serializable JSON
- Includes fallback for missing metadata
- Handles multiple drugs/events per case

---

## 4. Narrative Generation

**Requirement:**  
Generate human-readable case narratives from extracted AER fields.

**Implementation:**  
- Module: `4_narrative_generation/narrative_generator.py`
- Model: `Claude Sonnet` via AWS Bedrock
- Prompt constructed using `prompt_builder.py`
- Output passed into Vault-compliant narrative field

---

## 5. REST API Backend

**Requirement:**  
Provide upload, JSON generation, narrative generation, and download via an API.

**Implementation:**  
- Module: `5_rest_api/main.py` (FastAPI)
- Endpoints:
  - `POST /upload` — Upload literature
  - `GET /case/{id}` — Retrieve JSON
  - `POST /narrative?case_id=` — Generate narrative
  - `GET /download/case/{id}` / `narrative/{id}` — Download data
  - `POST /validate` — Submit feedback

---

## 6. Frontend UI

**Requirement:**  
Web interface to upload files, view outputs, and generate narrative with user-friendly interaction.

**Implementation:**  
- Stack: `Streamlit`
- Module: `6_streamlit/app.py`
- Connected to REST API
- Fully deployed at: [https://pharmacovigilence.com](https://pharmacovigilence.com)

---

## 7. Deployment

**Requirement:**  
Deploy full-stack app with HTTPS, routing, logging.

**Implementation:**  
- Backend and frontend Dockerized
- NGINX reverse proxy routes `/` to Streamlit and `/api/` to FastAPI
- HTTPS enabled with valid SSL certs
- Logs available via Docker

---

## 8. Output Format Compatibility

**Requirement:**  
Ensure output JSON complies with Vault AER JSON schema.

**Implementation:**  
- Template followed from `Deliverables/aer_case_schema.json`
- Output tested against multiple cases
- Final JSON and narrative downloadable

---

## Summary

| Requirement Area         | Status  |
|--------------------------|---------|
| Literature Ingestion     | ✅ Done |
| AER Entity Extraction    | ✅ Done |
| Case JSON Construction   | ✅ Done |
| Narrative Generation     | ✅ Done |
| API Backend              | ✅ Done |
| Frontend UI              | ✅ Done |
| HTTPS Deployment         | ✅ Done |
| Vault JSON Compatibility | ✅ Done |


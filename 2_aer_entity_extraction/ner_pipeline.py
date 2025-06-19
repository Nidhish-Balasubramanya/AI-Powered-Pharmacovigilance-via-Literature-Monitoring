from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
import spacy
import re

sci_nlp = spacy.load("en_core_sci_sm")

tokenizer = AutoTokenizer.from_pretrained("d4data/biomedical-ner-all")
model = AutoModelForTokenClassification.from_pretrained("d4data/biomedical-ner-all")
bert_pipeline = pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy="simple")

def extract_patient_info(text):
    age_match = re.search(r"Age:\s*(\d+)", text)
    sex_match = re.search(r"Sex:\s*(\w+)", text, re.I)
    weight_match = re.search(r"Weight:\s*(\d+(\.\d+)?)\s*kg", text, re.I)
    return {
        "age": age_match.group(1) if age_match else "",
        "sex": sex_match.group(1).capitalize() if sex_match else "",
        "weights": [weight_match.group(1)] if weight_match else []
    }

def extract_medical_history(text):
    history_match = re.search(r"Medical History:\s*(.+?)\.", text, re.DOTALL)
    return history_match.group(1).strip() if history_match else ""

def extract_entities(text):
    patient_info = extract_patient_info(text)
    med_history = extract_medical_history(text)
    narrative = text.strip().replace("\n", " ")

    result = {
        "drugs": [],
        "events": [],
        "test_results": [],
        "dates": [],
        "weights": patient_info["weights"],
        "units": [],
        "dosages": [],
        "sentences": [],
        "age": patient_info["age"],
        "sex": patient_info["sex"],
        "medical_history": med_history,
        "narrative": narrative
    }

    doc = sci_nlp(text)
    result["sentences"] = [sent.text for sent in doc.sents]

    for ent in doc.ents:
        label = ent.label_.lower()
        if "drug" in label or "chemical" in label:
            result["drugs"].append(ent.text)
        elif "disease" in label or "symptom" in label:
            result["events"].append(ent.text)
        elif "procedure" in label or "test" in label:
            result["test_results"].append(ent.text)

    bert_entities = bert_pipeline(text)
    for ent in bert_entities:
        word = ent["word"]
        label = ent["entity_group"]
        if word.startswith("##"):
            continue
        if label in ["CHEMICAL", "DRUG", "TREATMENT", "Therapeutic_procedure"]:
            result["drugs"].append(word)
        elif label in ["SYMPTOM", "DISEASE", "Sign_symptom"]:
            result["events"].append(word)
        elif label in ["TEST", "PROCEDURE", "Diagnostic_procedure"]:
            result["test_results"].append(word)
        elif label == "Lab_value":
            result["test_results"].append(word)

    for key in ["drugs", "events", "test_results"]:
        result[key] = list(set(result[key]))

    return result
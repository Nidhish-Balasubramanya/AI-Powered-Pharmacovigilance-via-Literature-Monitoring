import re

def extract_dates(text):
    return re.findall(r"\b\d{1,2}[-/ ]\w+[-/ ]\d{2,4}|\b\d{1,2}[-/]\d{1,2}[-/]\d{2,4}", text)

def extract_weights(text):
    return re.findall(r"\b\d+\s*(kg|lb|lbs)\b", text.lower())

def extract_units(text):
    return re.findall(r"\b\d+\s*(mg|g|ml|mcg|cm|mm)\b", text.lower())

def extract_dosages(text):
    return re.findall(r"\b\d+\s*(mg|ml)\s*(once|twice)?\s*(daily|per day|weekly)?", text.lower())

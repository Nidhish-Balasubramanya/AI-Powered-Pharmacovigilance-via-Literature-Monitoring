import os
import sys
import json
from pprint import pprint

sys.path.append(os.path.abspath('../2_AER_Entity_Extraction'))

from ner_pipeline import extract_entities
from json_generator import build_case_json  

text = """
A 34-year-old male was given Cholecap 100mg daily for two weeks.
He experienced nausea and fatigue on 15/08/2022.
An ECG test was conducted, and his weight was recorded as 58 kg.
"""

entities = extract_entities(text)
case_data = build_case_json(entities)

with open("vault_case_1.json", "w") as f:
    json.dump(case_data, f, indent=2)
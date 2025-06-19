from ner_pipeline import extract_entities

text = """
A 34-year-old male was given Cholecap 100mg daily for two weeks. 
He experienced nausea and fatigue on 15/08/2022. 
An ECG test was conducted, and his weight was recorded as 58 kg.
"""

entities = extract_entities(text)
from pprint import pprint
pprint(entities)

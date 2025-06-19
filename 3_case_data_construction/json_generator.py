import uuid

def build_case_json(entities: dict) -> dict:
    age = entities.get("age", "")
    sex = entities.get("sex", "")
    weight = entities.get("weights", [""])[0] if entities.get("weights") else ""
    drug = entities.get("drugs", [""])[0] if entities.get("drugs") else ""
    dosage_info = entities.get("dosages", [("", "", "")])[0] if entities.get("dosages") else ("", "", "")
    dosage = " ".join([x for x in dosage_info if x]).strip()
    events = entities.get("events", [])
    test_results = entities.get("test_results", [])
    report_date = entities.get("dates", [""])[0] if entities.get("dates") else ""
    med_history = entities.get("medical_history", "")
    narrative = entities.get("narrative", "")

    def format_events(events):
        return [
            {
                "event_reported__v": event,
                "country__v": "IN",
                "onset_idate__v": report_date,
                "serious__v": False,
                "outcome__v": "Unknown"
            }
            for event in events
        ]

    def format_tests(tests):
        return [
            {
                "test_name__v": test,
                "test_result__v": "Positive",
                "result_unit__v": "",
                "qualifier__v": "",
                "result_date__v": report_date
            }
            for test in tests
        ]

    contact_entry = {
        "qualification__v": "",
        "object_type__v": "reporter__v",
        "firstname_value__v": "",
        "middlename_value__v": "",
        "lastname_value__v": ""
    }

    parent_entry = {
        "case_medical_history__v": [],
        "case_drug_history__v": [],
        "age_value__v": age,
        "age_unit__v": "years",
        "dob_idate__v": "",
        "gender_value__v": sex,
        "height_value__v": "",
        "height_unit__v": "cm",
        "patient_id_value__v": "AA",
        "last_menstrual_normalized__v": "",
        "weight_value__v": weight,
        "weight_unit__v": "kg",
        "race__v": "",
        "ethnicity__v": "",
        "medical_history_text__v": med_history
    }

    transmission_entry = {
        "destination__v": "",
        "organization__v": "",
        "transmission_profile__v": "",
        "first_sender__v": "",
        "destination_transmission_id__v": "",
        "origin__v": "",
        "origin_transmission_id__v": "",
        "reason_text_long_text__v": "",
        "sender_comments__v": "",
        "recipient_user__v": "",
        "sender_user__v": ""
    }

    compliant_json = {
        "data": {
            "detail": {
                "structured": {
                    "narrative__v": narrative,
                    "case_classification__v": "Spontaneous",
                    "serious__v": False,
                    "seriousness_criteria__v": [],
                    "report_type__v": "Initial",
                    "receive_datetime__v": report_date,
                    "receipt_method__v": "Email",
                    "transmission_type__v": "Electronic"
                },
                "patient": {
                    "structured": {
                        "age_value__v": age,
                        "age_unit__v": "Years",
                        "gender_value__v": sex.capitalize(),
                        "weight__v": weight,
                        "weight_unit__v": "kg",
                        "patient_identifier__v": str(uuid.uuid4())
                    }
                },
                "case_product__v": {
                    "structured": [
                        {
                            "product_name__v": drug,
                            "dose_text__v": dosage,
                            "firstadmin_idate__v": report_date,
                            "indication_text__v": "",
                            "dose_unit__v": "mg",
                            "dose_number__v": 1
                        }
                    ]
                },
                "case_adverse_event__v": {
                    "structured": format_events(events)
                },
                "case_test_result__v": {
                    "structured": format_tests(test_results)
                },
                "case_contact__v": {
                    "structured": [contact_entry],
                    "metadata": {}
                },
                "parental_case__v": {
                    "structured": [parent_entry]
                },
                "transmission__v": {
                    "structured": [transmission_entry],
                    "metadata": {}
                }
            }
        }
    }
    return compliant_json
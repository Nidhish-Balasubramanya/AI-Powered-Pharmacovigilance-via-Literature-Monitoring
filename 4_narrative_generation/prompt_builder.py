import json
def build_prompt_from_json(data):
    return (
        "You are a pharmacovigilance expert. Based on the structured case report JSON below, "
        "generate a professional case narrative in natural language. "
        "Do not include field names or technical formatting. The narrative should read like a clinical summary, "
        "using medically appropriate language.\n\n"
        "Use complete sentences. If data is missing, omit the detail naturally or describe it as unavailable. "
        "Do not include placeholder phrases like 'not specified' unless it's meaningful.\n\n"
        "Here is the structured data:\n\n"
        f"{json.dumps(data, indent=2)}"
    )

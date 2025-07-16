import pandas as pd
import re

def extract_case_data(cases):
    records = []
    for case in cases:
        try:
            detail = case.get("data", {}).get("detail", {})
            patient = detail.get("patient", {}).get("structured", {})
            events = detail.get("case_adverse_event__v", {}).get("structured", [])
            narrative = detail.get("structured", {}).get("narrative__v", "")

            match = re.search(r'prescribed\s+([A-Za-z0-9\-]+)', narrative)
            drug_name = match.group(1) if match else "Unknown"

            raw_age = str(patient.get("age_value__v", "0")).strip()
            age = int(raw_age) if raw_age.isdigit() else 0
            sex = patient.get("gender_value__v", "Unknown")

            for event in events:
                records.append({
                    "drug": drug_name,
                    "age": age,
                    "sex": sex,
                    "reaction": event.get("event_reported__v", "Unknown"),
                    "outcome": event.get("outcome__v", "Unknown"),
                    "narrative": narrative
                })
        except Exception:
            continue
    return pd.DataFrame(records)

def generate_insights(df):
    df["age_group"] = pd.cut(df["age"], bins=[0, 20, 30, 45, 60, 75, 100],
                             labels=["0-20", "21-30", "31-45", "46-60", "61-75", "76-100"])
    return {
        "top_10_drugs": df["drug"].value_counts().head(10).to_dict(),
        "top_10_reactions": df["reaction"].value_counts().head(10).to_dict(),
        "outcome_by_gender": df.groupby("sex")["outcome"].value_counts().unstack().fillna(0).astype(int).to_dict(),
        "reaction_by_age": df.groupby("age_group")["reaction"].value_counts().unstack().fillna(0).astype(int).to_dict()
    }

def generate_summary_from_stats(stats):
    top_drugs = stats["top_10_drugs"]
    top_reactions = stats["top_10_reactions"]
    gender_data = stats["outcome_by_gender"]
    age_data = stats["reaction_by_age"]

    prompt = f"""
You are a pharmacovigilance analyst.

Based on the following statistical insights from a batch of adverse event reports, generate a multi-section **pharmacovigilance report**. It should have **detailed subheadings**, analytical paragraphs, and clear transitions.

The report must include:

1. **Top 10 Reported Drugs**
   - Mention the most frequent drugs
   - Discuss what this indicates about prescribing patterns
   - Subsection: **Drug Class Observations** (e.g., anti-diabetics, analgesics)

2. **Top 10 Adverse Reactions**
   - Describe the dominant adverse events
   - Highlight any surprising symptoms
   - Subsection: **Reaction Clusters by Body System** (e.g., neurological, gastrointestinal)

3. **Outcome by Gender**
   - Analyze differences in outcomes (e.g., recovery, hospitalization)
   - Subsection: **Disparities & Hypotheses** (e.g., why “other” gender has more hospitalizations)

4. **Reaction Patterns by Age Group**
   - Show which age groups had more or fewer reactions
   - Subsection: **Age-Specific Risk Factors** (e.g., polypharmacy in elderly)

5. **Notable Drug–Reaction Pairs**
   - Provide examples of frequently co-occurring drug + reaction combos

6. **Recommendations & Observational Insights**
   - Wrap up with 2–3 important takeaways for safety, demographic targeting, or future research

A very important thing u need to remeber is everytime a reques like this is generate make the heading BIgger than the content for easy reading avoid using emojis anywhere and make the document with in detail expanation and insights. more the content generated under each section th better.
Each section should be **descriptive and narrative-style**, and **reference the related chart or table**. DO NOT include any charts — the application will insert them later. Avoid repeating numbers — focus on analysis.
Here are the raw stats to use:

- Top Drugs: {top_drugs}
- Top Reactions: {top_reactions}
- Outcome by Gender: {gender_data}
- Reactions by Age: {age_data}
"""


    return prompt

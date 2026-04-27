import os
import json
from openai import OpenAI


ANALYSIS_PROMPT = """You are an academic paper analysis assistant. Analyze the following paper text and return a JSON object.

Paper text (first part):
{text}

Return ONLY a JSON object with this exact structure:
{{
  "title": "full paper title",
  "summary": "3-4 sentence structured summary covering main themes, methodology, and conclusions",
  "contributions": [
    "contribution 1",
    "contribution 2",
    "contribution 3",
    "contribution 4",
    "contribution 5"
  ],
  "reproducibility_score": 7.5,
  "code_availability": "HIGH",
  "datasets": "OPEN",
  "methodology_clarity": "VERY GOOD",
  "code_link": "https://github.com/... or N/A",
  "data_link": "https://... or N/A"
}}

For reproducibility_score use 0-10 scale.
For code_availability use: HIGH, MEDIUM, LOW, or NONE
For datasets use: OPEN, PARTIAL, or CLOSED
For methodology_clarity use: VERY GOOD, GOOD, FAIR, or POOR
"""


def analyze_paper_with_ai(text: str) -> dict | None:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None

    try:
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "user", "content": ANALYSIS_PROMPT.format(text=text[:8000])}
            ],
            response_format={"type": "json_object"},
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        return {"error": str(e)}

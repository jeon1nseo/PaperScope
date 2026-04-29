import re
import json
from openai import OpenAI


DEVELOPER_MESSAGE = "You are an academic paper analysis assistant. Output only valid JSON. No markdown, no explanation, no comments."

USER_MESSAGE_TEMPLATE = """Read the paper and output ONLY this JSON. No other text.
All Korean fields must be in Korean. score must be a number 0-100. difficulty must be one of: Beginner, Intermediate, Advanced.

{{"title":"paper title in Korean or English","summary":"2-3 sentence Korean summary","contribution1":"first contribution in Korean","contribution2":"second contribution in Korean","contribution3":"third contribution in Korean","dataset":"dataset availability in Korean","method_detail":"reproducibility explanation in Korean","code":"code availability in Korean","score":75,"score_reason":"reliability score reason in Korean","difficulty":"Intermediate","knowledge1":"required concept 1","knowledge2":"required concept 2","knowledge3":"required concept 3","query1":"english search query 1","query2":"english search query 2","query3":"english search query 3"}}

Paper text:
{text}"""


def _repair_json(raw: str) -> str:
    # Extract JSON block
    start = raw.find("{")
    end = raw.rfind("}") + 1
    if start == -1 or end == 0:
        return raw
    s = raw[start:end]
    # Remove trailing commas before } or ]
    s = re.sub(r",\s*([}\]])", r"\1", s)
    # Remove single-line comments
    s = re.sub(r"//[^\n]*", "", s)
    return s


def _flat_to_nested(d: dict) -> dict:
    """Convert flat LLM output to the nested structure analysis_panel expects."""
    return {
        "title": d.get("title", ""),
        "summary": d.get("summary", ""),
        "contributions": [
            v for k in ("contribution1", "contribution2", "contribution3")
            if (v := d.get(k, "").strip())
        ],
        "reproducibility": {
            "dataset_status": d.get("dataset", ""),
            "method_detail_level": d.get("method_detail", ""),
            "code_availability": d.get("code", ""),
        },
        "reliability": {
            "score": d.get("score", 0),
            "evaluation_reason": d.get("score_reason", ""),
        },
        "difficulty": {
            "level": d.get("difficulty", "Intermediate"),
            "required_knowledge": [
                v for k in ("knowledge1", "knowledge2", "knowledge3")
                if (v := d.get(k, "").strip())
            ],
            "reasoning": "",
        },
        "search_queries": [
            v for k in ("query1", "query2", "query3")
            if (v := d.get(k, "").strip())
        ],
    }


def analyze_paper_with_ai(text: str) -> dict | None:
    try:
        client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
        response = client.chat.completions.create(
            model="qwen2.5:7b",
            temperature=0,
            messages=[
                {"role": "system", "content": DEVELOPER_MESSAGE},
                {"role": "user", "content": USER_MESSAGE_TEMPLATE.format(text=text[:5000])}
            ],
        )
        content = response.choices[0].message.content
        fixed = _repair_json(content)
        flat = json.loads(fixed, strict=False)
        return _flat_to_nested(flat)
    except Exception as e:
        return {"error": str(e)}

import json
from openai import OpenAI


ANALYSIS_PROMPT = """당신은 엄격한 학술 논문 리뷰어이자 AI/머신러닝 전문가입니다. 아래 논문 텍스트({text})를 분석하여 엄격하게 구조화된 JSON만 반환하세요. 다른 텍스트는 절대 포함하지 마세요.

규칙:
- summary, contributions, 모든 설명 텍스트는 반드시 한국어로 작성
- JSON 키는 영어 유지
- difficulty.level은 반드시 Beginner, Intermediate, Advanced 중 하나

아래 구조의 JSON만 반환:
{{
  "title": "논문 제목 원문 그대로",
  "summary": "연구 목적, 제안 방법, 실험 결과, 결론을 포함한 3-4문장 요약 (한국어)",
  "contributions": [
    "핵심 기여 1 (한국어)",
    "핵심 기여 2 (한국어)",
    "핵심 기여 3 (한국어)",
    "핵심 기여 4 (한국어)",
    "핵심 기여 5 (한국어)"
  ],
  "reproducibility": {{
    "dataset_status": "데이터셋 공개 여부 및 접근 가능성 (한국어)",
    "method_detail_level": "실험 재현에 필요한 세부 정보 충실도 설명 (한국어)",
    "code_availability": "코드 공개 여부 (한국어)"
  }},
  "reliability": {{
    "score": 75,
    "evaluation_reason": "저자 신뢰도, 게재 학술지/학회 수준, 실험 근거, 이론적 타당성 기반 신뢰도 평가 (한국어)"
  }},
  "difficulty": {{
    "level": "Intermediate",
    "required_knowledge": ["필요 배경지식 1", "필요 배경지식 2", "필요 배경지식 3"],
    "reasoning": "난이도 판단 근거 (한국어)"
  }},
  "search_queries": ["관련 검색어 1", "관련 검색어 2", "관련 검색어 3"]
}}"""


def analyze_paper_with_ai(text: str) -> dict | None:
    try:
        client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
        response = client.chat.completions.create(
            model="llama3:latest",
            messages=[
                {"role": "user", "content": ANALYSIS_PROMPT.format(text=text[:8000])}
            ],
        )
        content = response.choices[0].message.content
        start = content.find("{")
        end = content.rfind("}") + 1
        return json.loads(content[start:end])
    except Exception as e:
        return {"error": str(e)}

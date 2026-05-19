import csv
import os
import urllib.parse
import requests

ALLOWED_KEYWORDS = [
    "ai", "artificial intelligence", "machine learning", "deep learning",
    "large language model", "llm", "transformer", "neural network",
    "computer vision", "reinforcement learning", "chatgpt", "gpt",
    "rag", "retrieval augmented generation", "retrieval-augmented generation",
    "nlp", "natural language processing", "diffusion model", "generative ai",
]

_FIELD_VISUALS = [
    (["medical", "clinical", "health", "drug", "biomedical"], ("EC4899", "8B5CF6"), "🏥", "의료 AI"),
    (["reinforcement", "reward", "policy"], ("10B981", "3B82F6"), "🎮", "강화학습"),
    (["graph", "molecule"], ("0369A1", "059669"), "🔗", "그래프 AI"),
    (["diffusion", "generative", "synthesis"], ("7C3AED", "DB2777"), "🎨", "생성 AI"),
    (["computer vision", "image", "visual", "segmentation", "detection"], ("0EA5E9", "6366F1"), "👁️", "컴퓨터 비전"),
    (["language", "text", "translation", "llm", "gpt", "bert", "transformer", "nlp"], ("2563EB", "7C3AED"), "🤖", "NLP"),
]
_DEFAULT_VISUAL = ("64748B", "334155"), "📄", "AI"

_rankings_cache: dict | None = None


def _load_rankings() -> dict:
    global _rankings_cache
    if _rankings_cache is not None:
        return _rankings_cache

    csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "journal_rankings.csv")
    result: dict = {}
    if not os.path.exists(csv_path):
        _rankings_cache = result
        return result

    with open(csv_path, encoding="utf-8-sig") as f:
        for row in csv.DictReader(f, delimiter=";"):
            issn_raw = row.get("Issn", "")
            for issn in issn_raw.replace(" ", "").split(","):
                issn = issn.replace("-", "").strip()
                if issn:
                    result[issn] = {
                        "scie": "Yes",
                        "quartile": row.get("SJR Best Quartile", ""),
                        "sjr_score": row.get("SJR", ""),
                    }

    _rankings_cache = result
    return result


def _find_rank(issn_list: list) -> dict:
    rankings = _load_rankings()
    for issn in issn_list:
        clean = issn.replace("-", "").strip()
        if clean in rankings:
            return rankings[clean]
    return {"scie": "정보 없음", "quartile": "", "sjr_score": ""}


def _restore_abstract(inverted_index: dict | None) -> str:
    if not inverted_index:
        return ""
    pairs = [(pos, word) for word, poses in inverted_index.items() for pos in poses]
    pairs.sort()
    return " ".join(word for _, word in pairs)


def _field_visual(title: str, abstract: str) -> tuple:
    text = (title + " " + abstract).lower()
    for keywords, colors, icon, name in _FIELD_VISUALS:
        if any(kw in text for kw in keywords):
            return colors, icon, name
    return _DEFAULT_VISUAL


def _normalize_quartile(q: str) -> str:
    if q in ("Q1", "Q2", "Q3"):
        return q
    if q == "Q4":
        return "Q3"
    return "Unknown"


def search_papers(query: str, max_results: int = 50) -> tuple[list[dict], str | None]:
    """OpenAlex에서 논문 검색. (papers, error_message) 반환."""
    q = query.strip().lower()
    if not q:
        return [], None

    if not any(kw in q for kw in ALLOWED_KEYWORDS):
        return [], "AI 관련 키워드를 입력하세요. (예: LLM, transformer, deep learning)"

    url = (
        f"https://api.openalex.org/works"
        f"?search={urllib.parse.quote(q)}&per-page={max_results}"
    )
    try:
        resp = requests.get(url, timeout=15)
        if resp.status_code != 200:
            return [], f"OpenAlex API 오류 (상태 코드: {resp.status_code})"
        data = resp.json()
    except requests.exceptions.Timeout:
        return [], "응답 시간 초과. 잠시 후 다시 시도해주세요."
    except requests.exceptions.RequestException as e:
        return [], f"네트워크 오류: {e}"

    papers: list[dict] = []
    for i, p in enumerate(data.get("results", [])):
        title = p.get("title", "")
        if not title:
            continue
        year = p.get("publication_year") or 0
        if year < 2020:
            continue

        abstract = _restore_abstract(p.get("abstract_inverted_index"))

        cited = p.get("cited_by_count") or 0
        doi = p.get("doi") or "DOI 없음"
        openalex_url = p.get("id", f"paper_{i}")

        journal, issn_list, pdf_url = "저널 없음", [], ""
        loc = p.get("primary_location")
        if loc:
            src = loc.get("source")
            if src:
                journal = src.get("display_name", "저널 없음")
                issn_list = src.get("issn") or []
            pdf_url = loc.get("pdf_url") or ""

        rank = _find_rank(issn_list)
        q_level = _normalize_quartile(rank["quartile"])

        authorships = p.get("authorships", [])
        authors_list = [
            a["author"]["display_name"]
            for a in authorships[:5]
            if a.get("author", {}).get("display_name")
        ] or ["저자 없음"]
        authors_str = ", ".join(authors_list[:3])
        if len(authors_list) > 3:
            authors_str += ", et al."

        colors, icon, field = _field_visual(title, abstract)
        score = (5 if q in title.lower() else 0) + abstract.lower().count(q) + cited // 1000

        papers.append({
            "id": openalex_url,
            "title": title,
            "authors": authors_str,
            "authors_list": authors_list,
            "citations": cited,
            "q_level": q_level,
            "journal": journal,
            "field": field,
            "year": year,
            "color": colors,
            "icon": icon,
            "doi": doi,
            "pdf_url": pdf_url,
            "abstract": abstract,
            "scie": rank["scie"],
            "sjr_score": rank["sjr_score"],
            "score": score,
        })

    papers.sort(key=lambda x: x["score"], reverse=True)
    return papers, None

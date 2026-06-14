import json
import requests
import urllib.parse
import csv
import os
import re
from bs4 import BeautifulSoup
from openai import OpenAI
from difflib import SequenceMatcher

RUNYOURAI_API_KEY = "runyour-v1-f00f09d0-daab-42a0-aad2-617190e9b13e-65fYlcsCikWpK93sI92CkN1glgvno1RoWa0bhT-NNd0zbEmRws0VqB3-EEYjhuSc"
RUNYOURAI_BASE_URL = "https://api.runyour.ai/v1"

runyour_client = OpenAI(
    api_key=RUNYOURAI_API_KEY,
    base_url=RUNYOURAI_BASE_URL
)

GROBID_URL = "http://localhost:8070/api/processFulltextDocument"

ALLOWED_KEYWORDS = [
    "ai", "artificial intelligence", "machine learning", "deep learning",
    "large language model", "llm", "transformer", "attention", "self-attention",
    "neural network", "computer vision", "reinforcement learning", "chatgpt",
    "gpt", "rag", "retrieval augmented generation", "retrieval-augmented generation",
    "nlp", "natural language processing", "diffusion model", "generative ai",
    "machine translation", "sequence transduction", "language model"
]


def restore_abstract(inverted_index):
    if not inverted_index:
        return "초록 없음"
    word_positions = []
    for word, positions in inverted_index.items():
        for position in positions:
            word_positions.append((position, word))
    word_positions.sort()
    words = [word for position, word in word_positions]
    return " ".join(words)


def load_journal_rankings(filename="journal_rankings.csv"):
    rankings = {}
    csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), filename)
    if not os.path.exists(csv_path):
        return rankings
    try:
        with open(csv_path, mode="r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f, delimiter=";")
            for row in reader:
                title = row.get("Title", "").strip().lower()
                if title:
                    rankings[title] = {
                        "q_level": row.get("SJR Best Quartile", "Unknown").strip(),
                        "scie": row.get("Overton", "No").strip(),
                        "sjr_score": row.get("SJR", "-").strip()
                    }
    except Exception as e:
        print(f"저널 CSV 로드 예외 발생: {e}")
    return rankings


def fetch_openalex_metadata(title: str) -> dict:
    journal_rankings = load_journal_rankings()
    default_res = {
        "citations": 0, "journal_name": "Unknown", "q_level": "Unknown",
        "scie": "No", "abstract": "초록 없음", "authors": [], "related_papers": []
    }

    if not title or title == "N/A":
        return default_res

    try:
        clean_title = title.strip().replace("\n", " ")
        encoded_title = urllib.parse.quote(clean_title)
        url = f"https://api.openalex.org/works?filter=title.search:{encoded_title}&per_page=5"

        res = requests.get(url, timeout=10)
        if res.status_code != 200:
            return default_res

        data = res.json()
        results = data.get("results", [])
        if not results:
            return default_res

        # 제목 유사도 기준 원논문 선택
        best_match = results[0]
        max_ratio = 0
        for paper in results:
            ratio = SequenceMatcher(None, clean_title.lower(), paper.get("title", "").lower()).ratio()
            if ratio > max_ratio:
                max_ratio = ratio
                best_match = paper

        citations = best_match.get("cited_by_count", 0)
        abstract_inverted = best_match.get("abstract_inverted_index")
        restored_abs = restore_abstract(abstract_inverted)

        # 저널명 추출
        venue_title = "Unknown"
        locations = best_match.get("locations", [])
        for loc in locations:
            source = loc.get("source")
            if source and source.get("display_name"):
                curr_venue = source.get("display_name").strip()
                if "arxiv" not in curr_venue.lower() and "cornell" not in curr_venue.lower():
                    venue_title = curr_venue
                    break
        if venue_title == "Unknown" and locations:
            venue_title = locations[0].get("source", {}).get("display_name", "Unknown")

        # CSV Q등급 매칭
        q_level = "Unknown"
        scie_status = "No"
        v_low = venue_title.lower()
        if v_low in journal_rankings:
            q_level = journal_rankings[v_low]["q_level"]
            scie_status = journal_rankings[v_low]["scie"]
        else:
            for csv_title, rank_info in journal_rankings.items():
                if csv_title in v_low or v_low in csv_title:
                    q_level = rank_info["q_level"]
                    scie_status = rank_info["scie"]
                    break

        # 저자 추출
        verified_authors = []
        for auth in best_match.get("authorships", []):
            a_name = auth.get("author", {}).get("display_name", "Unknown")
            institutions = auth.get("institutions", [])
            affil_name = institutions[0].get("display_name", "N/A") if institutions else "N/A"
            verified_authors.append({"name": a_name, "affiliation": affil_name})

        # 관련 논문 추천
        related_papers = []
        concepts = best_match.get("concepts", [])
        top_keywords = [c.get("display_name") for c in sorted(concepts, key=lambda x: x.get("score", 0), reverse=True)[:3]]

        if top_keywords:
            keyword_query = " AND ".join([f'"{k}"' for k in top_keywords])
            rec_url = f"https://api.openalex.org/works?filter=default_search:{urllib.parse.quote(keyword_query)}&per_page=10"
            rec_res = requests.get(rec_url, timeout=10)
            if rec_res.status_code == 200:
                for work in rec_res.json().get("results", []):
                    related_papers.append({
                        "id": work.get("id"),
                        "title": work.get("title"),
                        "authors": ", ".join([a.get("author", {}).get("display_name", "") for a in work.get("authorships", [])[:3]]),
                        "year": work.get("publication_year"),
                        "citations": work.get("cited_by_count", 0)
                    })

        return {
            "citations": citations, "journal_name": venue_title, "q_level": q_level,
            "scie": scie_status, "abstract": restored_abs, "authors": verified_authors,
            "related_papers": related_papers
        }
    except Exception:
        return default_res


def parse_pdf_via_grobid(pdf_bytes):
    try:
        files = {'input': ('paper.pdf', pdf_bytes, 'application/pdf')}
        data = {'consolidateHeader': '1', 'consolidateCitations': '1', 'includeRawCitations': '1'}
        response = requests.post(GROBID_URL, files=files, data=data, timeout=30)
        if response.status_code != 200:
            return None
        soup = BeautifulSoup(response.text, 'xml')

        parsed_data = {
            "metadata": {"title": "N/A", "journal": "N/A", "doi": "N/A", "authors": []},
            "body": {"Abstract": "", "Introduction": "", "Methodology": "", "Dataset": "", "Experiment": "", "Conclusion": ""}
        }

        header = soup.find('teiHeader')
        if header:
            title_tag = header.find('title', attrs={'level': 'a', 'type': 'main'})
            if title_tag:
                parsed_data["metadata"]["title"] = title_tag.get_text(strip=True)
            doi_tag = header.find('idno', attrs={'type': 'DOI'})
            if doi_tag:
                parsed_data["metadata"]["doi"] = doi_tag.get_text(strip=True)
            journal_tag = header.find('title', attrs={'level': 'j'})
            if journal_tag:
                parsed_data["metadata"]["journal"] = journal_tag.get_text(strip=True)
            for author in header.find_all('author'):
                author_dict = {"name": "N/A", "affiliation": "N/A"}
                p_name = author.find('persName')
                if p_name:
                    fname = " ".join([f.get_text(strip=True) for f in p_name.find_all('forename')])
                    sname = p_name.find('surname').get_text(strip=True) if p_name.find('surname') else ""
                    author_dict["name"] = f"{fname} {sname}".strip()
                org = author.find('orgName', attrs={'type': 'institution'})
                if org:
                    author_dict["affiliation"] = org.get_text(strip=True)
                if author_dict["name"] != "N/A":
                    parsed_data["metadata"]["authors"].append(author_dict)

        body_tag = soup.find('body')
        if body_tag:
            for div in body_tag.find_all('div'):
                head = div.find('head')
                if not head:
                    continue
                raw_title = head.get_text(strip=True)
                title_low = raw_title.lower()
                section_content = "\n".join([p.get_text(separator=' ', strip=True) for p in div.find_all('p')])
                if not section_content:
                    continue
                formatted_text = f"\n[{raw_title}]\n{section_content}\n"
                if any(kw in title_low for kw in ["dataset", "data source", "corpus", "data set", "material"]):
                    parsed_data["body"]["Dataset"] += formatted_text
                elif any(kw in title_low for kw in ["experiment", "result", "evaluat", "performance", "finding", "discussion"]):
                    parsed_data["body"]["Experiment"] += formatted_text
                elif any(kw in title_low for kw in ["intro", "background", "related work", "literature"]):
                    parsed_data["body"]["Introduction"] += formatted_text
                elif any(kw in title_low for kw in ["method", "approach", "proposed", "model", "architecture", "framework", "design"]):
                    parsed_data["body"]["Methodology"] += formatted_text
                elif any(kw in title_low for kw in ["conclu", "summary", "future work"]):
                    parsed_data["body"]["Conclusion"] += formatted_text
        return parsed_data
    except Exception:
        return None


def analyze_paper_with_runyour_ai(parsed_data, model_id="openai/gpt-4.1-2025-04-14") -> dict:
    developer_instruction = """You are a highly rigorous academic reviewer and AI/machine learning expert. Your task is to analyze the structured paper sections provided in JSON format and extract specific evaluation metrics into a strictly structured JSON format.

[CRITICAL PRESENTATION & UI SAFETY RULES]
1. Comprehensive yet Summarized: Maintain deep analytical judgments but present them as high-density summarized texts.
2. Predicate Style Rule:
   - contributions: 각 항목은 "~를 제시함.", "~를 밝힘.", "~를 입증함." 으로 끝낼 것
   - summary: 자연스러운 한국어 완전한 문장
   - 나머지 서술 필드: "~임." 으로 끝낼 것

[SCORING]
1. Reproducibility Score: 10~100 사이 정수 (10 단위)
2. Reliability Score: 10~100 사이 정수 (10 단위)
3. Difficulty: Beginner / Intermediate / Advanced 중 택1

[REQUIRED OUTPUT SCHEMA]
{
  "summary": "3~4줄 한국어 요약",
  "contributions": ["기여1", "기여2", "기여3"],
  "reproducibility": {
    "score": 80,
    "dataset_status": "...",
    "method_detail_level": "...",
    "code_availability": "..."
  },
  "reliability": {
    "score": 90,
    "evaluation_reason": "..."
  },
  "difficulty": {
    "reasoning": "...",
    "level": "Intermediate",
    "required_knowledge": ["개념1", "개념2"]
  },
  "search_queries": ["query1", "query2", "query3"]
}"""

    pdf_title = parsed_data["metadata"]["title"]
    openalex_info = fetch_openalex_metadata(pdf_title)

    final_authors = parsed_data["metadata"]["authors"]
    if not final_authors or any(a.get("affiliation") == "N/A" for a in final_authors):
        if openalex_info["authors"]:
            final_authors = openalex_info["authors"]

    payload_body = {
        "metadata": {
            "title": pdf_title if pdf_title != "N/A" else "Unknown Title",
            "grobid_journal": parsed_data["metadata"]["journal"],
            "doi": parsed_data["metadata"]["doi"],
            "authors": final_authors
        },
        "openalex_verified_metadata": {
            "real_citations": openalex_info["citations"],
            "verified_journal": openalex_info["journal_name"],
            "journal_q_level": openalex_info["q_level"],
            "journal_scie": openalex_info["scie"],
            "restored_abstract_context": openalex_info["abstract"]
        },
        "body": {
            "abstract": parsed_data["body"]["Abstract"],
            "introduction": parsed_data["body"]["Introduction"],
            "methodology": parsed_data["body"]["Methodology"],
            "dataset": parsed_data["body"]["Dataset"],
            "experiment": parsed_data["body"]["Experiment"],
            "conclusion": parsed_data["body"]["Conclusion"]
        }
    }

    try:
        response = runyour_client.chat.completions.create(
            model=model_id,
            response_format={"type": "json_object"},
            messages=[
                {"role": "developer", "content": developer_instruction},
                {"role": "user", "content": f"Analyze this paper:\n{json.dumps(payload_body, ensure_ascii=False)}"}
            ],
            temperature=0.2
        )

        final_json = json.loads(response.choices[0].message.content)

        # 점수 정규화
        rep_val = 80
        if "reproducibility" in final_json and isinstance(final_json["reproducibility"], dict):
            rep_val = final_json["reproducibility"].get("score", 80)
            try:
                rep_val = int(float(str(rep_val).split("/")[0]))
            except:
                rep_val = 80
            if rep_val <= 10:
                rep_val *= 10
            final_json["reproducibility"]["score"] = int(rep_val)

        rel_val = 80
        if "reliability" in final_json and isinstance(final_json["reliability"], dict):
            try:
                rel_val = int(float(final_json["reliability"].get("score", 80)))
            except:
                rel_val = 80
            final_json["reliability"]["score"] = rel_val

        final_json["reproducibility_score"] = int(rep_val)
        final_json["reliability_score"] = int(rel_val)
        final_json["recommended_papers_pool"] = openalex_info["related_papers"]
        return final_json

    except Exception as e:
        return {"error": f"분석 실패: {str(e)}"}

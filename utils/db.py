import os
import logging
from dotenv import load_dotenv
from supabase import create_client, Client

# .env 로드
load_dotenv()

# 로거 설정
logger = logging.getLogger(__name__)

# 환경변수 읽기 + 검증
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError(
        "Supabase 환경변수가 설정되지 않았습니다. "
        ".env 파일에 SUPABASE_URL과 SUPABASE_KEY를 확인하세요."
    )

# Supabase 클라이언트
try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    logger.error(f"Supabase 클라이언트 생성 실패: {e}")
    raise RuntimeError(f"Supabase 연결 실패: {e}") from e


# ===== Bookmarks =====

def get_bookmarks(user_email: str) -> list:
    """사용자의 북마크 목록을 최신순으로 반환."""
    if not user_email:
        return []
    try:
        res = (
            supabase.table("bookmarks")
            .select("*")
            .eq("user_email", user_email)
            .order("created_at", desc=True)
            .execute()
        )
        return res.data or []
    except Exception as e:
        logger.error(f"get_bookmarks 실패 (user={user_email}): {e}")
        return []


def add_bookmark(user_email: str, paper: dict) -> bool:
    """북마크 추가. 성공 시 True, 실패 시 False."""
    if not user_email or not paper:
        return False

    paper_id = str(paper.get("id", "")).strip()
    if not paper_id:
        logger.warning("add_bookmark: paper_id가 비어있음")
        return False

    try:
        supabase.table("bookmarks").insert({
            "user_email": user_email,
            "paper_id": paper_id,
            "title": paper.get("title", ""),
            "authors": paper.get("authors", ""),
            "journal": paper.get("journal", ""),
            "year": paper.get("year"),
            "citations": paper.get("citations"),
            "q_level": paper.get("q_level", ""),
            "field": paper.get("field", ""),
            "abstract": paper.get("abstract", ""),
            "doi": paper.get("doi", ""),
            "pdf_url": paper.get("pdf_url", ""),
        }).execute()
        return True
    except Exception as e:
        logger.error(f"add_bookmark 실패 (user={user_email}, paper={paper_id}): {e}")
        return False


def remove_bookmark(user_email: str, paper_id: str) -> bool:
    """북마크 제거. 성공 시 True, 실패 시 False."""
    if not user_email or not paper_id:
        return False
    try:
        supabase.table("bookmarks").delete().eq(
            "user_email", user_email
        ).eq("paper_id", str(paper_id)).execute()
        return True
    except Exception as e:
        logger.error(f"remove_bookmark 실패 (user={user_email}, paper={paper_id}): {e}")
        return False

def is_bookmarked(user_email: str, paper_id: str) -> bool:
    """특정 논문이 이미 북마크 되어 있는지 확인."""
    if not user_email or not paper_id:
        return False
    try:
        res = (
            supabase.table("bookmarks")
            .select("id")
            .eq("user_email", user_email)
            .eq("paper_id", str(paper_id))
            .limit(1)
            .execute()
        )
        return bool(res.data)
    except Exception as e:
        logger.error(f"is_bookmarked 실패 (user={user_email}, paper={paper_id}): {e}")
        return False

# ===== PDF History =====

def get_pdf_history(user_email: str) -> list:
    """사용자의 PDF 분석 기록을 최신순으로 반환."""
    if not user_email:
        return []
    try:
        res = (
            supabase.table("pdf_history")
            .select("*")
            .eq("user_email", user_email)
            .order("created_at", desc=True)
            .execute()
        )
        return res.data or []
    except Exception as e:
        logger.error(f"get_pdf_history 실패 (user={user_email}): {e}")
        return []

def add_pdf_history(user_email: str, pdf_name: str, analysis: dict) -> bool:
    """PDF 분석 기록 저장. 성공 시 True, 실패 시 False."""
    if not user_email or not pdf_name:
        return False
    try:
        supabase.table("pdf_history").insert({
            "user_email": user_email,
            "pdf_name": pdf_name,
            "reliability_score": analysis.get("reliability_score"),
            "reproducibility_score": analysis.get("reproducibility_score"),
            "analysis": analysis,
        }).execute()
        return True
    except Exception as e:
        logger.error(f"add_pdf_history 실패 (user={user_email}, pdf={pdf_name}): {e}")
        return False

def delete_pdf_history(user_email: str, history_id: str) -> bool:
    """PDF 분석 기록 삭제."""
    if not user_email or not history_id:
        return False
    try:
        supabase.table("pdf_history").delete().eq(
            "user_email", user_email
        ).eq("id", history_id).execute()
        return True
    except Exception as e:
        logger.error(f"delete_pdf_history 실패 (user={user_email}, id={history_id}): {e}")
        return False

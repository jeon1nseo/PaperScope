import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def get_bookmarks(user_email: str) -> list:
    try:
        res = supabase.table("bookmarks").select("*").eq("user_email", user_email).execute()
        return res.data or []
    except:
        return []


def add_bookmark(user_email: str, paper: dict):
    try:
        supabase.table("bookmarks").insert({
            "user_email": user_email,
            "paper_id": str(paper.get("id", "")),
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
    except:
        pass


def remove_bookmark(user_email: str, paper_id: str):
    try:
        supabase.table("bookmarks").delete().eq("user_email", user_email).eq("paper_id", paper_id).execute()
    except:
        pass


def get_pdf_history(user_email: str) -> list:
    try:
        res = supabase.table("pdf_history").select("*").eq("user_email", user_email).order("created_at", desc=True).execute()
        return res.data or []
    except:
        return []


def add_pdf_history(user_email: str, pdf_name: str, analysis: dict):
    try:
        supabase.table("pdf_history").insert({
            "user_email": user_email,
            "pdf_name": pdf_name,
            "reliability_score": analysis.get("reliability_score"),
            "reproducibility_score": analysis.get("reproducibility_score"),
            "analysis": analysis,
        }).execute()
    except:
        pass

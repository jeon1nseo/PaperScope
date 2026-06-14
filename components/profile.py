import streamlit as st
from utils.db import get_pdf_history, get_bookmarks, remove_bookmark


def render_profile():
    st.markdown("""
    <div style='background:#1E293B; padding:20px 28px; border-radius:16px; margin-bottom:24px; display:flex; align-items:center; gap:16px;'>
      <div>
        <div style='font-size:20px; font-weight:800; color:white;'>{}</div>
        <div style='font-size:13px; color:#94A3B8; margin-top:2px;'>{}</div>
      </div>
    </div>
    """.format(
        st.session_state.get("user_nickname", ""),
        st.session_state.get("user_email", "")
    ), unsafe_allow_html=True)

    user_email = st.session_state.get("user_email", "")
    tab1, tab2 = st.tabs(["📄 분석 히스토리", "🔖 북마크"])

    # ── 분석 히스토리 ──
    with tab1:
        # Supabase에서 불러오기 (없으면 session_state 폴백)
        db_history = get_pdf_history(user_email) if user_email else []
        if db_history:
            history = db_history
        else:
            history = st.session_state.get("pdf_history", [])
        if not history:
            st.markdown("""
            <div style='text-align:center; color:#94A3B8; padding:40px 0;'>
              <div style='font-size:32px; margin-bottom:8px;'>📄</div>
              <div style='font-size:14px;'>아직 분석한 논문이 없어요</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            for idx, item in enumerate(history):
                # Supabase row vs session_state dict 둘 다 처리
                name = item.get("pdf_name") or item.get("name", "")
                reliability = item.get("reliability_score") or item.get("reliability", "-")
                reproducibility = item.get("reproducibility_score") or item.get("reproducibility", "-")
                date_str = str(item.get("created_at", "") or item.get("date", ""))[:16]
                analysis = item.get("analysis") or {}

                with st.container(border=True):
                    st.markdown(f"**{name}**")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.caption(f"🛡️ 신뢰도 {reliability}/100")
                    with col2:
                        st.caption(f"🧪 재현성 {reproducibility}/100")
                    with col3:
                        st.caption(f"📅 {date_str}")
                    if st.button("결과 다시 보기", key=f"hist_{idx}_{name}"):
                        st.session_state.pdf_analysis = analysis
                        st.session_state.pdf_name = name
                        st.session_state.selected_paper = "pdf"
                        st.session_state.page = "main"
                        st.rerun()

    # ── 북마크 ──
    with tab2:
        # Supabase에서 불러오기 (없으면 session_state 폴백)
        db_bookmarks = get_bookmarks(user_email) if user_email else []
        if db_bookmarks:
            bookmarks = db_bookmarks
        else:
            bookmarks = st.session_state.get("bookmarks", [])
        if not bookmarks:
            st.markdown("""
            <div style='text-align:center; color:#94A3B8; padding:40px 0;'>
              <div style='font-size:32px; margin-bottom:8px;'>🔖</div>
              <div style='font-size:14px;'>북마크한 논문이 없어요</div>
              <div style='font-size:12px; margin-top:4px;'>논문 목록에서 ★ 버튼을 눌러 저장하세요</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            for bm_idx, paper in enumerate(bookmarks):
                # Supabase row: paper_id 컬럼 / session_state: id 컬럼
                paper_id = str(paper.get("paper_id") or paper.get("id", ""))
                with st.container(border=True):
                    q = paper.get("q_level", "")
                    q_label = {"Q1": "🟢 Q1", "Q2": "🟡 Q2", "Q3": "🟠 Q3"}.get(q, "")
                    citations = paper.get("citations", 0) or 0
                    st.markdown(f"**{paper.get('title', '')}**")
                    st.caption(f"👥 {paper.get('authors', '')}  |  ⭐ {citations:,}  |  {q_label}  |  {paper.get('year', '')}")
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("상세보기", key=f"bm_view_{bm_idx}_{paper_id}"):
                            # analysis_panel이 쓰는 형식으로 맞춰서 넘김
                            view_paper = dict(paper)
                            view_paper["id"] = paper_id
                            st.session_state.selected_paper = paper_id
                            st.session_state.selected_real_paper = view_paper
                            st.session_state.page = "main"
                            st.rerun()
                    with col2:
                        paper_id = str(paper.get("paper_id") or paper.get("id", ""))
                        if st.button("북마크 삭제", key=f"bm_del_{bm_idx}_{paper_id[:20]}"):
                            remove_bookmark(user_email, paper_id)
                            st.session_state.bookmarks = [p for p in st.session_state.get("bookmarks", []) if str(p.get("id", "")) != paper_id]
                            st.rerun()

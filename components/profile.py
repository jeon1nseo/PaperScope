import streamlit as st


def render_profile():
    st.markdown("""
    <div style='background:#1E293B; padding:24px 28px; border-radius:16px; margin-bottom:24px;'>
      <div style='font-size:40px; margin-bottom:8px;'>👤</div>
      <div style='font-size:22px; font-weight:800; color:white;'>{}</div>
      <div style='font-size:14px; color:#94A3B8; margin-top:4px;'>{}</div>
    </div>
    """.format(
        st.session_state.get("user_nickname", ""),
        st.session_state.get("user_email", "")
    ), unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["📄 분석 히스토리", "🔖 북마크"])

    # ── 분석 히스토리 ──
    with tab1:
        history = st.session_state.get("pdf_history", [])
        if not history:
            st.markdown("""
            <div style='text-align:center; color:#94A3B8; padding:40px 0;'>
              <div style='font-size:32px; margin-bottom:8px;'>📄</div>
              <div style='font-size:14px;'>아직 분석한 논문이 없어요</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            for item in reversed(history):
                with st.container(border=True):
                    st.markdown(f"**{item['name']}**")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.caption(f"🛡️ 신뢰도 {item.get('reliability', '-')}/100")
                    with col2:
                        st.caption(f"🧪 재현성 {item.get('reproducibility', '-')}/100")
                    with col3:
                        st.caption(f"📅 {item.get('date', '')}")
                    if st.button("결과 다시 보기", key=f"hist_{item['name']}_{item.get('date','')}"):
                        st.session_state.pdf_analysis = item.get("analysis")
                        st.session_state.pdf_name = item["name"]
                        st.session_state.selected_paper = "pdf"
                        st.session_state.page = "main"
                        st.rerun()

    # ── 북마크 ──
    with tab2:
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
            for paper in bookmarks:
                with st.container(border=True):
                    q = paper.get("q_level", "")
                    q_label = {"Q1": "🟢 Q1", "Q2": "🟡 Q2", "Q3": "🟠 Q3"}.get(q, "")
                    st.markdown(f"**{paper['title']}**")
                    st.caption(f"👥 {paper.get('authors', '')}  |  ⭐ {paper.get('citations', 0):,}  |  {q_label}  |  {paper.get('year', '')}")
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("상세보기", key=f"bm_view_{paper['id']}"):
                            st.session_state.selected_paper = paper["id"]
                            st.session_state.selected_real_paper = paper
                            st.session_state.page = "main"
                            st.rerun()
                    with col2:
                        if st.button("북마크 삭제", key=f"bm_del_{paper['id']}"):
                            st.session_state.bookmarks = [p for p in bookmarks if p["id"] != paper["id"]]
                            st.rerun()

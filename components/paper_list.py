import streamlit as st
from utils.pdf_parser import extract_text_from_pdf
from utils.ai_analyzer import analyze_paper_with_ai

DUMMY_PAPERS = [
    {
        "id": 1,
        "title": "Transformers for Large-Scale Text Classification: A Survey",
        "authors": "A. Sharma, J. Lee, et al.",
        "citations": 2456,
        "q_level": "Q1",
        "journal": "Computer Vision and Pattern Recognition",
        "field": "NLP",
        "year": 2023,
        "color": ("2563EB", "7C3AED"),
        "icon": "🤖",
    },
    {
        "id": 2,
        "title": "Self-Supervised Learning in Medical Imaging",
        "authors": "A. Sharma, A. Lee, et al.",
        "citations": 1120,
        "q_level": "Q2",
        "journal": "Medical Informatics",
        "field": "의료 AI",
        "year": 2022,
        "color": ("059669", "0891B2"),
        "icon": "🧬",
    },
    {
        "id": 3,
        "title": "Efficient Neural Architecture Search for Edge Devices",
        "authors": "A. Sharma, J. Lee, et al.",
        "citations": 2456,
        "q_level": "Q2",
        "journal": "Computer Vision and AI Recognition",
        "field": "컴퓨터 비전",
        "year": 2023,
        "color": ("D97706", "DC2626"),
        "icon": "⚡",
    },
    {
        "id": 4,
        "title": "Diffusion Models for Image Synthesis: A Comprehensive Review",
        "authors": "B. Kim, C. Park, et al.",
        "citations": 3812,
        "q_level": "Q1",
        "journal": "Neural Information Processing Systems",
        "field": "생성 AI",
        "year": 2023,
        "color": ("7C3AED", "DB2777"),
        "icon": "🎨",
    },
    {
        "id": 5,
        "title": "Graph Neural Networks in Drug Discovery",
        "authors": "D. Choi, E. Jung, et al.",
        "citations": 987,
        "q_level": "Q3",
        "journal": "Bioinformatics",
        "field": "의료 AI",
        "year": 2022,
        "color": ("0369A1", "059669"),
        "icon": "💊",
    },
    {
        "id": 6,
        "title": "CLIP: Learning Transferable Visual Models From Natural Language",
        "authors": "A. Radford, J. Kim, et al.",
        "citations": 8921,
        "q_level": "Q1",
        "journal": "International Conference on Machine Learning",
        "field": "컴퓨터 비전",
        "year": 2021,
        "color": ("0EA5E9", "6366F1"),
        "icon": "👁️",
    },
    {
        "id": 7,
        "title": "Attention Is All You Need",
        "authors": "A. Vaswani, N. Shazeer, et al.",
        "citations": 62340,
        "q_level": "Q1",
        "journal": "Advances in Neural Information Processing Systems",
        "field": "NLP",
        "year": 2017,
        "color": ("F59E0B", "EF4444"),
        "icon": "✨",
    },
    {
        "id": 8,
        "title": "LoRA: Low-Rank Adaptation of Large Language Models",
        "authors": "E. Hu, Y. Shen, et al.",
        "citations": 5678,
        "q_level": "Q1",
        "journal": "International Conference on Learning Representations",
        "field": "NLP",
        "year": 2022,
        "color": ("10B981", "3B82F6"),
        "icon": "🔧",
    },
    {
        "id": 9,
        "title": "Segment Anything Model for Medical Image Segmentation",
        "authors": "M. Chen, L. Wang, et al.",
        "citations": 432,
        "q_level": "Q2",
        "journal": "Medical Image Analysis",
        "field": "의료 AI",
        "year": 2024,
        "color": ("EC4899", "8B5CF6"),
        "icon": "🏥",
    },
    {
        "id": 10,
        "title": "Reinforcement Learning from Human Feedback for Code Generation",
        "authors": "S. Park, H. Yoon, et al.",
        "citations": 234,
        "q_level": "Q3",
        "journal": "Empirical Software Engineering",
        "field": "강화학습",
        "year": 2024,
        "color": ("64748B", "334155"),
        "icon": "💻",
    },
]

BADGE_CLASS = {"Q1": "badge-q1", "Q2": "badge-q2", "Q3": "badge-q3"}
ALL_FIELDS = sorted(set(p["field"] for p in DUMMY_PAPERS))
ALL_YEARS = sorted(set(p["year"] for p in DUMMY_PAPERS), reverse=True)


def _thumbnail(color_start, color_end, icon):
    return f"""
    <div style='
        background: linear-gradient(135deg, #{color_start}, #{color_end});
        border-radius: 8px;
        width: 72px; min-width: 72px; height: 88px;
        display: flex; align-items: center; justify-content: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.15);
    '>
        <span style='font-size:32px;'>{icon}</span>
    </div>"""


def render_paper_list():
    tab_upload, tab_browse = st.tabs(["📂 PDF 업로드", "🔍 논문 목록"])

    # ── PDF 업로드 탭 ──────────────────────────────────────────
    with tab_upload:
        uploaded = st.file_uploader(
            "논문 PDF를 업로드하세요",
            type=["pdf"],
            label_visibility="collapsed",
        )

        if uploaded is not None:
            if st.session_state.get("pdf_name") != uploaded.name:
                with st.spinner("PDF 텍스트 추출 중..."):
                    text = extract_text_from_pdf(uploaded)
                    st.session_state.pdf_text = text
                    st.session_state.pdf_name = uploaded.name
                    st.session_state.pdf_analysis = None

                if text.startswith("[오류]"):
                    st.error(text)
                else:
                    import os
                    if os.getenv("OPENAI_API_KEY"):
                        with st.spinner("AI 분석 중... (30초~1분 소요)"):
                            analysis = analyze_paper_with_ai(text)
                            st.session_state.pdf_analysis = analysis
                    st.session_state.selected_paper = "pdf"
                    st.rerun()
            else:
                st.success(f"✅ {uploaded.name} 업로드 완료!")
                st.caption(f"추출된 텍스트: {len(st.session_state.pdf_text):,}자")
                if st.button("📊 AI 분석 보기", use_container_width=True, type="primary"):
                    st.session_state.selected_paper = "pdf"
                    st.rerun()
        else:
            st.markdown("""
            <div style='border:2px dashed #CBD5E1; border-radius:10px;
                        padding:40px 20px; text-align:center; color:#94A3B8;'>
              <div style='font-size:36px; margin-bottom:8px;'>📄</div>
              <div style='font-size:14px; font-weight:600;'>PDF 파일을 드래그하거나 클릭해서 업로드</div>
              <div style='font-size:12px; margin-top:4px;'>지원 형식: PDF</div>
            </div>
            """, unsafe_allow_html=True)

    # ── 논문 목록 탭 ───────────────────────────────────────────
    with tab_browse:
        # 검색창
        search_query = st.text_input(
            "검색",
            placeholder="🔍  제목, 저자, 저널로 검색...",
            label_visibility="collapsed",
            key="paper_search",
        )

        # 필터 행
        f1, f2, f3, f4 = st.columns(4)
        with f1:
            q_filter = st.selectbox(
                "저널 등급",
                ["전체", "Q1", "Q2", "Q3"],
                key="filter_q",
                label_visibility="collapsed",
            )
        with f2:
            field_filter = st.selectbox(
                "분야",
                ["전체 분야"] + ALL_FIELDS,
                key="filter_field",
                label_visibility="collapsed",
            )
        with f3:
            year_filter = st.selectbox(
                "연도",
                ["전체 연도"] + [str(y) for y in ALL_YEARS],
                key="filter_year",
                label_visibility="collapsed",
            )
        with f4:
            sort_filter = st.selectbox(
                "정렬",
                ["인용수 높은순", "인용수 낮은순", "최신순", "오래된순"],
                key="filter_sort",
                label_visibility="collapsed",
            )

        # 필터 적용
        filtered = DUMMY_PAPERS[:]

        if search_query.strip():
            q = search_query.lower()
            filtered = [
                p for p in filtered
                if q in p["title"].lower()
                or q in p["authors"].lower()
                or q in p["journal"].lower()
            ]
        if q_filter != "전체":
            filtered = [p for p in filtered if p["q_level"] == q_filter]
        if field_filter != "전체 분야":
            filtered = [p for p in filtered if p["field"] == field_filter]
        if year_filter != "전체 연도":
            filtered = [p for p in filtered if p["year"] == int(year_filter)]

        # 정렬 적용
        if sort_filter == "인용수 높은순":
            filtered.sort(key=lambda p: p["citations"], reverse=True)
        elif sort_filter == "인용수 낮은순":
            filtered.sort(key=lambda p: p["citations"])
        elif sort_filter == "최신순":
            filtered.sort(key=lambda p: p["year"], reverse=True)
        elif sort_filter == "오래된순":
            filtered.sort(key=lambda p: p["year"])

        # 헤더
        h_col, c_col = st.columns([2, 1])
        with h_col:
            st.markdown(
                f"<span style='font-weight:700; font-size:15px; color:#1E293B;'>논문 목록</span>",
                unsafe_allow_html=True,
            )
        with c_col:
            st.markdown(
                f"<span style='font-size:12px; color:#94A3B8; float:right;'>{len(filtered)}개 결과</span>",
                unsafe_allow_html=True,
            )

        if not filtered:
            st.markdown(
                "<div style='text-align:center; color:#94A3B8; padding:40px 0;'>검색 결과가 없습니다.</div>",
                unsafe_allow_html=True,
            )

        # 논문 카드
        for paper in filtered:
            badge_cls = BADGE_CLASS.get(paper["q_level"], "badge-q2")
            is_selected = st.session_state.selected_paper == paper["id"]
            card_cls = "paper-card selected" if is_selected else "paper-card"
            thumb = _thumbnail(paper["color"][0], paper["color"][1], paper["icon"])

            st.markdown(f"""
            <div class="{card_cls}" style='display:flex; gap:14px; align-items:flex-start;'>
              {thumb}
              <div style='flex:1; min-width:0;'>
                <div class="paper-title">{paper['title']}</div>
                <div class="paper-authors">👥 {paper['authors']}</div>
                <div class="paper-meta">
                  <span class="paper-citations">⭐ {paper['citations']:,} citations</span>
                  <span class="{badge_cls}">{paper['q_level']}</span>
                  <span style="color:#64748B; font-size:11px;">{paper['field']} · {paper['year']}</span>
                </div>
              </div>
            </div>
            """, unsafe_allow_html=True)

            if st.button("📊 AI 분석", key=f"analyze_{paper['id']}", use_container_width=True):
                st.session_state.selected_paper = paper["id"]
                st.rerun()

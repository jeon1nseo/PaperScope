import html
import io
import streamlit as st
from utils.pdf_parser import extract_text_from_pdf, extract_first_page_image
from utils.ai_analyzer import analyze_paper_with_ai
from utils.paper_search import search_papers

BADGE_CLASS = {"Q1": "badge-q1", "Q2": "badge-q2", "Q3": "badge-q3"}


def _thumbnail(title, authors, color_start, color_end):
    t = html.escape(title[:55] + "..." if len(title) > 55 else title)
    a = html.escape(authors[:30] + "..." if len(authors) > 30 else authors)
    return (
        f"<div style='background:white;border:1px solid #E2E8F0;border-radius:8px;"
        f"width:72px;min-width:72px;height:88px;overflow:hidden;"
        f"box-shadow:0 2px 8px rgba(0,0,0,0.10);display:flex;flex-direction:column;padding:6px;'>"
        f"<div style='font-size:5.5px;font-weight:700;color:#1E293B;line-height:1.45;margin-bottom:5px;word-break:break-word;'>{t}</div>"
        f"<div style='height:1px;background:#E2E8F0;margin-bottom:4px;'></div>"
        f"<div style='font-size:4.5px;color:#64748B;line-height:1.4;'>{a}</div>"
        f"</div>"
    )


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
                    pdf_bytes = uploaded.read()
                    text = extract_text_from_pdf(io.BytesIO(pdf_bytes))
                    img_b64 = extract_first_page_image(pdf_bytes)
                    st.session_state.pdf_text = text
                    st.session_state.pdf_name = uploaded.name
                    st.session_state.pdf_analysis = None
                    st.session_state.pdf_first_page = img_b64

                if text.startswith("[오류]"):
                    st.error(text)
                else:
                    with st.spinner("AI 분석 중... (1~2분 소요)"):
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
        # 세션 상태 초기화
        if "search_results" not in st.session_state:
            st.session_state.search_results = []
        if "last_search_query" not in st.session_state:
            st.session_state.last_search_query = ""
        if "search_error" not in st.session_state:
            st.session_state.search_error = ""

        # 검색창 + 버튼
        sq_col, btn_col = st.columns([4, 1])
        with sq_col:
            search_query = st.text_input(
                "검색",
                placeholder="🔍  LLM, transformer, deep learning ...",
                label_visibility="collapsed",
                key="paper_search",
            )
        with btn_col:
            do_search = st.button("검색", use_container_width=True, type="primary")

        if do_search and search_query.strip():
            if search_query.strip() != st.session_state.last_search_query:
                with st.spinner("OpenAlex에서 논문 검색 중..."):
                    results, err = search_papers(search_query.strip())
                st.session_state.search_results = results
                st.session_state.last_search_query = search_query.strip()
                st.session_state.search_error = err or ""
                st.rerun()

        if st.session_state.search_error:
            st.warning(st.session_state.search_error)

        papers_pool = st.session_state.search_results

        if not papers_pool:
            st.markdown("""
            <div style='text-align:center; color:#94A3B8; padding:40px 0;'>
              <div style='font-size:32px; margin-bottom:8px;'>🔍</div>
              <div style='font-size:14px; font-weight:600;'>키워드를 입력하고 검색 버튼을 눌러주세요</div>
              <div style='font-size:12px; margin-top:4px;'>예: LLM, transformer, computer vision</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            # 동적 필터 옵션
            all_fields = sorted(set(p["field"] for p in papers_pool))
            all_years = sorted(set(p["year"] for p in papers_pool), reverse=True)

            # 필터 행
            f1, f2, f3, f4 = st.columns(4)
            with f1:
                q_filter = st.selectbox(
                    "저널 등급",
                    ["전체", "Q1", "Q2", "Q3", "Unknown"],
                    key="filter_q",
                    label_visibility="collapsed",
                )
            with f2:
                field_filter = st.selectbox(
                    "분야",
                    ["전체 분야"] + all_fields,
                    key="filter_field",
                    label_visibility="collapsed",
                )
            with f3:
                year_filter = st.selectbox(
                    "연도",
                    ["전체 연도"] + [str(y) for y in all_years],
                    key="filter_year",
                    label_visibility="collapsed",
                )
            with f4:
                sort_filter = st.selectbox(
                    "정렬",
                    ["관련도순", "인용수 높은순", "인용수 낮은순", "최신순", "오래된순"],
                    key="filter_sort",
                    label_visibility="collapsed",
                )

            # 필터 적용
            filtered = papers_pool[:]
            if q_filter != "전체":
                filtered = [p for p in filtered if p["q_level"] == q_filter]
            if field_filter != "전체 분야":
                filtered = [p for p in filtered if p["field"] == field_filter]
            if year_filter != "전체 연도":
                filtered = [p for p in filtered if p["year"] == int(year_filter)]

            if sort_filter == "관련도순":
                filtered.sort(key=lambda p: p["score"], reverse=True)
            elif sort_filter == "인용수 높은순":
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
                    f"<span style='font-weight:700; font-size:15px; color:#1E293B;'>검색 결과: <b>{st.session_state.last_search_query}</b></span>",
                    unsafe_allow_html=True,
                )
            with c_col:
                st.markdown(
                    f"<span style='font-size:12px; color:#94A3B8; float:right;'>{len(filtered)}개 결과</span>",
                    unsafe_allow_html=True,
                )

            if not filtered:
                st.markdown(
                    "<div style='text-align:center; color:#94A3B8; padding:40px 0;'>필터 조건에 맞는 논문이 없습니다.</div>",
                    unsafe_allow_html=True,
                )

            # 논문 카드
            for paper in filtered:
                is_selected = st.session_state.selected_paper == paper["id"]
                with st.container(border=True):
                    thumb_col, info_col = st.columns([1, 5])
                    with thumb_col:
                        thumb = _thumbnail(paper["title"], paper["authors"], paper["color"][0], paper["color"][1])
                        st.markdown(thumb, unsafe_allow_html=True)
                    with info_col:
                        q = paper["q_level"]
                        scie = "🔵 SCIE" if paper.get("scie") == "Yes" else ""
                        q_label = {"Q1": "🟢 Q1", "Q2": "🟡 Q2", "Q3": "🟠 Q3"}.get(q, "")
                        st.markdown(f"**{paper['title']}**")
                        st.caption(f"👥 {paper['authors']}")
                        st.caption(f"⭐ {paper['citations']:,} citations　　{q_label}　{scie}　　{paper['field']} · {paper['year']}")
                    if st.button("📊 논문 상세보기", key=f"analyze_{paper['id']}", use_container_width=True):
                        st.session_state.selected_paper = paper["id"]
                        st.session_state.selected_real_paper = paper
                        st.rerun()

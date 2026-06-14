import streamlit as st


def _render_real_paper(paper: dict):
    """논문 목록에서 선택한 논문 상세 표시"""
    q = paper.get("q_level", "")
    scie = "🔵 SCIE" if paper.get("scie") == "Yes" else ""
    q_label = {"Q1": "🟢 Q1", "Q2": "🟡 Q2", "Q3": "🟠 Q3"}.get(q, q)

    st.markdown(f"""
    <div style='background:white; border-radius:12px; padding:24px;
                box-shadow:0 2px 8px rgba(0,0,0,0.08); margin-bottom:16px;'>
      <div style='font-size:18px; font-weight:800; color:#0F172A; margin-bottom:8px;'>{paper.get('title','')}</div>
      <div style='font-size:13px; color:#64748B; margin-bottom:8px;'>👥 {paper.get('authors','')}</div>
      <div style='font-size:13px; color:#64748B; margin-bottom:12px;'>
        ⭐ {paper.get('citations',0):,} citations &nbsp;|&nbsp; {q_label} {scie} &nbsp;|&nbsp; {paper.get('field','')} · {paper.get('year','')}
      </div>
      <div style='font-size:13px; color:#475569; margin-bottom:4px;'>📰 {paper.get('journal','')}</div>
    </div>
    """, unsafe_allow_html=True)

    abstract = paper.get("abstract", "")
    if abstract:
        st.markdown(f"""
        <div style='background:#F8FAFC; border-radius:10px; padding:16px; border:1px solid #E2E8F0; margin-bottom:12px;'>
          <div style='font-size:13px; font-weight:700; color:#334155; margin-bottom:8px;'>📋 초록</div>
          <div style='font-size:13px; color:#475569; line-height:1.7;'>{abstract}</div>
        </div>
        """, unsafe_allow_html=True)

    doi = paper.get("doi", "")
    pdf_url = paper.get("pdf_url", "")
    col1, col2 = st.columns(2)
    with col1:
        if doi and doi != "DOI 없음":
            st.link_button("🔗 DOI 링크", doi, use_container_width=True)
    with col2:
        if pdf_url:
            st.link_button("📄 PDF 다운로드", pdf_url, use_container_width=True)


def render_analysis_panel():
    selected = st.session_state.get("selected_paper")

    # 논문 목록에서 선택한 경우
    if selected and selected != "pdf":
        paper = st.session_state.get("selected_real_paper")
        if paper:
            if st.button("✕ 닫기", key="close_real_paper"):
                st.session_state.selected_paper = None
                st.session_state.selected_real_paper = None
                st.rerun()
            _render_real_paper(paper)
            return

    if selected != "pdf" or "pdf_analysis" not in st.session_state or not st.session_state.pdf_analysis:
        st.markdown("""
        <div style='background: #FFFFFF; border-radius: 16px; padding: 80px 24px;
                    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05); text-align: center; border: 1px solid #F1F5F9;'>
          <div style='font-size: 56px; margin-bottom: 20px;'>📄</div>
          <div style='font-size: 20px; font-weight: 700; color: #0F172A; margin-bottom: 10px;'>
            AI Analysis Dashboard
          </div>
          <div style='font-size: 14px; color: #64748B; max-width: 360px; margin: 0 auto; line-height: 1.6;'>
            PDF 논문을 드롭하시면 OpenAlex 인프라 검증 지표가 융합된 AI 정밀 심사 결과가 여기에 표시됩니다.
          </div>
        </div>
        """, unsafe_allow_html=True)
        return

    analysis = st.session_state.pdf_analysis

    if "error" in analysis:
        st.error(f"🚨 AI 분석 오류: {analysis['error']}")
        return

    st.markdown("""
    <div style='margin-bottom: 28px;'>
        <h2 style='color: #0F172A; font-size: 24px; font-weight: 800; letter-spacing: -0.03em; margin: 0;'>
            📊 AI 정밀 심사 리포트
        </h2>
        <p style='color: #64748B; font-size: 13px; margin: 4px 0 0 0;'>OpenAlex 인용 데이터 및 4대 기둥 교차 검증 기반 정량 보고서</p>
    </div>
    """, unsafe_allow_html=True)

    repro_score = int(analysis.get("reproducibility_score", 80))
    reli_score = int(analysis.get("reliability_score", 80))

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
                    border-radius: 12px; padding: 18px; border: 1px solid #BFDBFE; margin-bottom: 10px;'>
            <div style='font-size: 13px; font-weight: 700; color: #1E40AF;'>🛡️ 신뢰도 점수 (Reliability)</div>
            <div style='font-size: 28px; font-weight: 900; color: #1D4ED8; margin-top: 4px;'>{reli_score} <span style='font-size: 16px; font-weight: 500; color: #1E40AF;'>/ 100</span></div>
        </div>
        """, unsafe_allow_html=True)
        st.progress(reli_score / 100)

    with col2:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #FDF4FF 0%, #F5D0FE 100%);
                    border-radius: 12px; padding: 18px; border: 1px solid #F59E0B; margin-bottom: 10px;'>
            <div style='font-size: 13px; font-weight: 700; color: #86198F;'>🧪 재현성 점수 (Reproducibility)</div>
            <div style='font-size: 28px; font-weight: 900; color: #701A75; margin-top: 4px;'>{repro_score} <span style='font-size: 16px; font-weight: 500; color: #86198F;'>/ 100</span></div>
        </div>
        """, unsafe_allow_html=True)
        st.progress(repro_score / 100)

    st.markdown("<div style='margin-top: 32px;'></div>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📝 논문 요약 & 기여", "🔍 신뢰성 & 재현성 검증", "🔗 연관 추천 풀"])

    with tab1:
        st.markdown("""
        <div style='background: #F8FAFC; border-radius: 12px; padding: 20px; border: 1px solid #E2E8F0; margin-top: 12px;'>
            <div style='font-size: 15px; font-weight: 700; color: #334155; margin-bottom: 8px;'>📝 논문 교차 요약</div>
            <div style='font-size: 14px; color: #475569; line-height: 1.6; white-space: pre-wrap;'>{}</div>
        </div>
        """.format(analysis.get("summary", "요약 정보가 없습니다.")), unsafe_allow_html=True)

        st.markdown("<div style='font-size: 15px; font-weight: 700; color: #334155; margin-top: 24px; margin-bottom: 10px;'>🚀 핵심 기여도 (Contributions)</div>", unsafe_allow_html=True)
        for contrib in analysis.get("contributions", []):
            st.markdown(f"""
            <div style='background: white; border-left: 4px solid #2563EB; padding: 10px 14px; margin-bottom: 8px;
                        box-shadow: 0 1px 3px rgba(0,0,0,0.02); border-radius: 0 8px 8px 0; font-size: 13.5px; color: #334155;'>
                {contrib}
            </div>
            """, unsafe_allow_html=True)

    with tab2:
        st.markdown("<div style='font-size: 15px; font-weight: 700; color: #334155; margin-top: 12px; margin-bottom: 12px;'>🧪 재현성 정밀 진단</div>", unsafe_allow_html=True)
        repro_data = analysis.get("reproducibility", {})
        if isinstance(repro_data, dict):
            st.markdown(f"**💡 방법론 기술 밀도:** {repro_data.get('method_detail_level', 'N/A')}")
            st.markdown(f"**📊 데이터셋 가용성:** {repro_data.get('dataset_status', 'N/A')}")
            st.markdown(f"**💻 오픈소스 코드 상태:** {repro_data.get('code_availability', 'N/A')}")

        st.markdown("<div style='font-size: 15px; font-weight: 700; color: #334155; margin-top: 24px; margin-bottom: 12px;'>🛡️ 신뢰성 심사 근거 리포트</div>", unsafe_allow_html=True)
        reli_data = analysis.get("reliability", {})
        if isinstance(reli_data, dict):
            st.markdown(f"""
            <div style='background: #F8FAFC; border-radius: 10px; padding: 16px; border: 1px solid #E2E8F0;
                        font-size: 13.5px; color: #475569; line-height: 1.6;'>
                {reli_data.get('evaluation_reason', '세부 근거가 없습니다.')}
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='font-size: 15px; font-weight: 700; color: #334155; margin-top: 24px; margin-bottom: 12px;'>📊 논문 독해 난이도 평가</div>", unsafe_allow_html=True)
        diff_data = analysis.get("difficulty", {})
        if isinstance(diff_data, dict):
            level = diff_data.get("level", "Intermediate")
            if level == "Advanced":
                st.error(f"🔥 난이도 등급: {level}")
            elif level == "Intermediate":
                st.warning(f"⚡ 난이도 등급: {level}")
            else:
                st.success(f"🌱 난이도 등급: {level}")
            st.markdown(f"**⚙️ 판별 근거:** {diff_data.get('reasoning', 'N/A')}")
            st.markdown(f"**📚 권장 선행 지식:** {', '.join(diff_data.get('required_knowledge', []))}")

    with tab3:
        st.markdown("<div style='font-size: 15px; font-weight: 700; color: #334155; margin-top: 12px; margin-bottom: 12px;'>🔍 학술 확장 검색 쿼리</div>", unsafe_allow_html=True)
        queries = analysis.get("search_queries", [])
        if len(queries) >= 3:
            st.info(f"🌐 **대분류:** `{queries[0]}`")
            st.success(f"⚡ **중분류:** `{queries[1]}`")
            st.warning(f"🎯 **소분류:** `{queries[2]}`")

        st.markdown("<div style='font-size: 15px; font-weight: 700; color: #047857; margin-top: 24px; margin-bottom: 12px;'>🔗 OpenAlex 키워드 기반 추천 논문</div>", unsafe_allow_html=True)
        pool = analysis.get("recommended_papers_pool", [])
        if pool:
            for idx, p in enumerate(pool, 1):
                with st.expander(f"📚 {idx}. {p.get('title')}"):
                    st.markdown(f"**👤 저자:** {p.get('authors')}")
                    st.markdown(f"**📅 연도:** {p.get('year')}년")
                    st.markdown(f"**🔥 인용수:** {p.get('citations')}회")
        else:
            st.info("추천된 연관 논문이 없습니다.")

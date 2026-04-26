import streamlit as st

# 더미 분석 데이터 (나중에 OpenAI API로 교체)
DUMMY_ANALYSIS = {
    1: {
        "title": "Transformers for Large-Scale Text Classification: A Survey",
        "summary": (
            "This survey provides a comprehensive analysis of transformer-based architectures "
            "for large-scale text classification tasks. The paper examines state-of-the-art methods, "
            "benchmark comparisons across major NLP datasets, and highlights the trade-offs between "
            "model size, computational efficiency, and classification accuracy."
        ),
        "contributions": [
            "Introduces a novel transformer-based attention mechanism for long documents",
            "Proposes a benchmark dataset for large-scale open-domain classification",
            "Establishes new state-of-the-art results on 5 major benchmarks",
            "Deduces new transformer architecture for edge deployment",
            "Proposes new efficiency metrics for academic and industry evaluation",
        ],
        "reproducibility_score": 8.2,
        "code_availability": "HIGH",
        "datasets": "OPEN",
        "methodology_clarity": "VERY GOOD",
        "code_link": "https://github.com/example/transformer-text-cls",
        "data_link": "https://huggingface.co/datasets/example",
    }
}


def render_analysis_panel():
    # PDF 업로드 모드
    if st.session_state.selected_paper == "pdf":
        pdf_name = st.session_state.get("pdf_name", "업로드된 논문")
        pdf_text = st.session_state.get("pdf_text", "")
        st.markdown(f"""
        <div style='background:white; border-radius:12px; padding:24px;
                    box-shadow:0 2px 8px rgba(0,0,0,0.08);'>
          <div style='font-size:12px; color:#2563EB; font-weight:600; margin-bottom:6px;'>
            📄 업로드된 PDF
          </div>
          <div style='font-size:17px; font-weight:700; color:#1E293B; margin-bottom:20px;'>
            {pdf_name}
          </div>
          <div class="section-card">
            <div class="section-title">📋 추출된 텍스트 미리보기</div>
            <div style='font-size:12px; color:#334155; line-height:1.7;
                        max-height:200px; overflow-y:auto; white-space:pre-wrap;'>
              {pdf_text[:1000]}{'...' if len(pdf_text) > 1000 else ''}
            </div>
          </div>
          <div class="section-card" style='text-align:center; color:#94A3B8;'>
            <div style='font-size:24px; margin-bottom:8px;'>🤖</div>
            <div style='font-weight:600; color:#1E293B; margin-bottom:4px;'>AI 분석 준비 중</div>
            <div style='font-size:13px;'>OpenAI API 연결 후 자동으로 분석 결과가 표시됩니다.</div>
          </div>
        </div>
        """, unsafe_allow_html=True)
        return

    if st.session_state.selected_paper is None:
        st.markdown("""
        <div style='background:white; border-radius:12px; padding:60px 24px;
                    box-shadow:0 2px 8px rgba(0,0,0,0.08); text-align:center;'>
          <div style='font-size:48px; margin-bottom:16px;'>📄</div>
          <div style='font-size:18px; font-weight:700; color:#1E293B; margin-bottom:8px;'>
            AI Analysis
          </div>
          <div style='font-size:14px; color:#94A3B8;'>
            왼쪽에서 논문을 선택하면 AI 분석 결과가 여기에 표시됩니다.
          </div>
        </div>
        """, unsafe_allow_html=True)
        return

    paper_id = st.session_state.selected_paper
    analysis = DUMMY_ANALYSIS.get(paper_id)

    if analysis is None:
        st.info("이 논문의 분석 데이터를 준비 중입니다.")
        return

    # 패널 헤더
    st.markdown(f"""
    <div style='background:white; border-radius:12px; padding:24px;
                box-shadow:0 2px 8px rgba(0,0,0,0.08);'>
      <div style='display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:20px;'>
        <div>
          <div style='font-size:12px; color:#2563EB; font-weight:600; margin-bottom:6px;'>
            ✨ AI-Powered Paper Analysis
          </div>
          <div style='font-size:17px; font-weight:700; color:#1E293B; line-height:1.4;'>
            {analysis['title']}
          </div>
        </div>
      </div>
    """, unsafe_allow_html=True)

    # 구조화된 요약
    st.markdown(f"""
      <div class="section-card">
        <div class="section-title">📋 STRUCTURED SUMMARY</div>
        <div style='font-size:13px; color:#334155; line-height:1.7;'>{analysis['summary']}</div>
      </div>
    """, unsafe_allow_html=True)

    # 핵심 기여 + 재현성 점수 (2열)
    contrib_col, repro_col = st.columns([1.2, 1])

    with contrib_col:
        contributions_html = "".join(
            f"<li style='margin-bottom:6px; color:#334155; font-size:13px;'>{c}</li>"
            for c in analysis["contributions"]
        )
        st.markdown(f"""
        <div class="section-card" style='height:100%;'>
          <div class="section-title">🔑 KEY CONTRIBUTIONS</div>
          <div style='font-size:12px; color:#94A3B8; margin-bottom:8px;'>
            Unique novelties or major findings:
          </div>
          <ul style='padding-left:16px; margin:0;'>
            {contributions_html}
          </ul>
        </div>
        """, unsafe_allow_html=True)

    with repro_col:
        score = analysis["reproducibility_score"]
        st.markdown(f"""
        <div class="section-card" style='height:100%;'>
          <div class="section-title">✅ REPRODUCIBILITY SCORE</div>
          <div class="repro-score">
            <span class="score-number">{score}</span>
            <span class="score-max"> / 10</span>
            <div class="score-label">(0-10 scale)</div>
          </div>
          <div class="metric-row">
            <div class="metric-item">
              <div class="metric-value">{analysis['code_availability']}</div>
              <div class="metric-label">CODE AVAILABILITY</div>
            </div>
            <div class="metric-item">
              <div class="metric-value">{analysis['datasets']}</div>
              <div class="metric-label">DATASETS</div>
            </div>
            <div class="metric-item">
              <div class="metric-value">{analysis['methodology_clarity']}</div>
              <div class="metric-label">METHODOLOGY CLARITY</div>
            </div>
          </div>
          <div style='margin-top:14px; font-size:11px; color:#64748B; line-height:1.6;'>
            Code: <a href="{analysis['code_link']}" style='color:#2563EB;'>{analysis['code_link']}</a><br/>
            Data: <a href="{analysis['data_link']}" style='color:#2563EB;'>{analysis['data_link']}</a>
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

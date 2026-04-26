import streamlit as st

# 논문별 썸네일 색상/아이콘 (paper_list.py와 동일하게 유지)
PAPER_VISUALS = {
    1: {"color": ("2563EB", "7C3AED"), "icon": "🤖"},
    2: {"color": ("059669", "0891B2"), "icon": "🧬"},
    3: {"color": ("D97706", "DC2626"), "icon": "⚡"},
    4: {"color": ("7C3AED", "DB2777"), "icon": "🎨"},
    5: {"color": ("0369A1", "059669"), "icon": "💊"},
}

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

    visual = PAPER_VISUALS.get(paper_id, {"color": ("2563EB", "7C3AED"), "icon": "📄"})
    c1, c2 = visual["color"]
    icon = visual["icon"]

    # 패널 헤더 (썸네일 이미지 포함)
    st.markdown(f"""
    <div style='background:white; border-radius:12px; padding:24px;
                box-shadow:0 2px 8px rgba(0,0,0,0.08);'>
      <div style='display:flex; gap:20px; align-items:flex-start; margin-bottom:20px;'>
        <div style='
            background: linear-gradient(135deg, #{c1}, #{c2});
            border-radius:12px; min-width:110px; height:140px;
            display:flex; flex-direction:column;
            align-items:center; justify-content:center; gap:8px;
            box-shadow: 0 4px 16px rgba(0,0,0,0.15);
        '>
          <span style='font-size:40px;'>{icon}</span>
          <span style='font-size:9px; color:rgba(255,255,255,0.8);
                       font-weight:700; letter-spacing:0.05em;'>RESEARCH PAPER</span>
        </div>
        <div style='flex:1;'>
          <div style='font-size:12px; color:#2563EB; font-weight:600; margin-bottom:6px;'>
            ✨ AI-Powered Paper Analysis
          </div>
          <div style='font-size:16px; font-weight:700; color:#1E293B; line-height:1.5; margin-bottom:12px;'>
            {analysis['title']}
          </div>
          <div style='display:flex; gap:8px; flex-wrap:wrap;'>
            <span style='background:#EFF6FF; color:#2563EB; padding:3px 10px;
                         border-radius:12px; font-size:11px; font-weight:600;'>📄 PDF</span>
            <span style='background:#F0FDF4; color:#15803D; padding:3px 10px;
                         border-radius:12px; font-size:11px; font-weight:600;'>✅ 분석 완료</span>
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

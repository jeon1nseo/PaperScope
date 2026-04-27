import streamlit as st

PAPER_VISUALS = {
    1: {"color": ("2563EB", "7C3AED"), "icon": "🤖"},
    2: {"color": ("059669", "0891B2"), "icon": "🧬"},
    3: {"color": ("D97706", "DC2626"), "icon": "⚡"},
    4: {"color": ("7C3AED", "DB2777"), "icon": "🎨"},
    5: {"color": ("0369A1", "059669"), "icon": "💊"},
}

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
    },
    2: {
        "title": "Self-Supervised Learning in Medical Imaging",
        "summary": (
            "This paper investigates self-supervised learning (SSL) techniques applied to medical imaging tasks "
            "including CT, MRI, and X-ray classification. The authors propose a contrastive pretraining strategy "
            "that outperforms supervised baselines with significantly fewer labeled samples, demonstrating strong "
            "generalization across multiple clinical datasets."
        ),
        "contributions": [
            "Proposes MedSSL: a domain-specific self-supervised pretraining framework for medical images",
            "Achieves 94.3% diagnostic accuracy with only 10% labeled data on chest X-ray benchmark",
            "Introduces medical image-specific augmentation pipeline for contrastive learning",
            "Demonstrates cross-modality transfer (CT → MRI) with minimal fine-tuning",
            "Releases large-scale unlabeled medical imaging dataset (500K+ images)",
        ],
        "reproducibility_score": 7.5,
        "code_availability": "HIGH",
        "datasets": "PARTIAL",
        "methodology_clarity": "GOOD",
        "code_link": "https://github.com/example/medssl",
        "data_link": "N/A (institutional approval required)",
    },
    3: {
        "title": "Efficient Neural Architecture Search for Edge Devices",
        "summary": (
            "This work presents an efficient NAS framework targeting resource-constrained edge devices. "
            "The proposed method combines hardware-aware search with once-for-all supernet training to reduce "
            "search cost by 300x compared to prior methods, while achieving Pareto-optimal accuracy-latency "
            "trade-offs on mobile and IoT hardware."
        ),
        "contributions": [
            "Proposes HW-NAS: hardware-aware neural architecture search with device-specific proxy metrics",
            "Reduces NAS search cost from 300 GPU-days to under 1 GPU-day via progressive shrinking",
            "Achieves 72.1% top-1 ImageNet accuracy at 15ms latency on Cortex-M55",
            "Introduces unified supernet that supports 10,000+ sub-networks without retraining",
            "Provides NAS benchmark across 8 edge hardware targets",
        ],
        "reproducibility_score": 6.8,
        "code_availability": "MEDIUM",
        "datasets": "OPEN",
        "methodology_clarity": "GOOD",
        "code_link": "https://github.com/example/hw-nas",
        "data_link": "https://image-net.org",
    },
    4: {
        "title": "Diffusion Models for Image Synthesis: A Comprehensive Review",
        "summary": (
            "A thorough review of score-based and denoising diffusion probabilistic models (DDPMs) for "
            "high-fidelity image synthesis. The survey categorizes 80+ methods across unconditional generation, "
            "text-to-image, image editing, and video synthesis tasks, and provides a unified theoretical framework "
            "connecting diffusion models to stochastic differential equations."
        ),
        "contributions": [
            "Unified theoretical framework linking DDPMs, score matching, and stochastic differential equations",
            "Taxonomy of 80+ diffusion-based methods across 12 application domains",
            "Comprehensive benchmark comparison on FID, CLIP score, and human evaluation metrics",
            "Analysis of sampling acceleration techniques (DDIM, DPM-Solver, consistency models)",
            "Open-source evaluation toolkit supporting 15 diffusion model baselines",
        ],
        "reproducibility_score": 9.1,
        "code_availability": "HIGH",
        "datasets": "OPEN",
        "methodology_clarity": "VERY GOOD",
        "code_link": "https://github.com/example/diffusion-survey",
        "data_link": "https://huggingface.co/datasets/laion",
    },
    5: {
        "title": "Graph Neural Networks in Drug Discovery",
        "summary": (
            "This paper applies graph neural networks (GNNs) to molecular property prediction and drug-target "
            "interaction modeling. By representing molecules as graphs with atom nodes and bond edges, the proposed "
            "AttentiveFP-based architecture achieves state-of-the-art performance on 11 MoleculeNet benchmarks, "
            "accelerating virtual screening pipelines by 40x."
        ),
        "contributions": [
            "Proposes MolGNN: an attentive graph neural network for molecular property prediction",
            "State-of-the-art results on 11/15 MoleculeNet benchmark tasks",
            "Novel graph-level readout mechanism capturing both local and global molecular features",
            "Drug-target interaction prediction achieving 0.92 AUC on BindingDB",
            "Open-source toolkit integrating with RDKit and DeepChem for virtual screening",
        ],
        "reproducibility_score": 7.9,
        "code_availability": "HIGH",
        "datasets": "OPEN",
        "methodology_clarity": "GOOD",
        "code_link": "https://github.com/example/molgnn",
        "data_link": "https://moleculenet.org",
    },
}


def _render_analysis(analysis: dict, visual: dict):
    c1, c2 = visual["color"]
    icon = visual["icon"]

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
          <span style='font-size:48px;'>{icon}</span>
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

    st.markdown(f"""
      <div class="section-card">
        <div class="section-title">📋 STRUCTURED SUMMARY</div>
        <div style='font-size:13px; color:#334155; line-height:1.7;'>{analysis['summary']}</div>
      </div>
    """, unsafe_allow_html=True)

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


def render_analysis_panel():
    # 닫기 버튼 (논문 선택된 경우)
    if st.session_state.selected_paper is not None:
        close_col, _ = st.columns([0.12, 0.88])
        with close_col:
            if st.button("✕ 닫기", key="close_panel"):
                st.session_state.selected_paper = None
                st.session_state.pdf_text = ""
                st.session_state.pdf_name = ""
                st.session_state.pdf_analysis = None
                st.rerun()

    # PDF 업로드 모드
    if st.session_state.selected_paper == "pdf":
        pdf_name = st.session_state.get("pdf_name", "업로드된 논문")
        pdf_text = st.session_state.get("pdf_text", "")
        pdf_analysis = st.session_state.get("pdf_analysis")

        if pdf_analysis and "error" not in pdf_analysis:
            visual = {"color": ("2563EB", "7C3AED"), "icon": "📄"}
            _render_analysis(pdf_analysis, visual)
            return

        # 분석 결과 없을 때 (API 키 미설정 or 오류)
        import os
        has_api_key = bool(os.getenv("OPENAI_API_KEY"))

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
        </div>
        """, unsafe_allow_html=True)

        if not has_api_key:
            st.warning("AI 분석을 사용하려면 OPENAI_API_KEY 환경변수를 설정해주세요.\n\n터미널에서: `export OPENAI_API_KEY='sk-...'`")
        elif pdf_analysis and "error" in pdf_analysis:
            st.error(f"AI 분석 오류: {pdf_analysis['error']}")
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
    visual = PAPER_VISUALS.get(paper_id, {"color": ("2563EB", "7C3AED"), "icon": "📄"})

    if analysis is None:
        st.info("이 논문의 분석 데이터를 준비 중입니다.")
        return

    _render_analysis(analysis, visual)

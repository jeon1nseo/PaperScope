import streamlit as st

PAPER_VISUALS = {
    1: {"color": ("2563EB", "7C3AED"), "icon": "🤖"},
    2: {"color": ("059669", "0891B2"), "icon": "🧬"},
    3: {"color": ("D97706", "DC2626"), "icon": "⚡"},
    4: {"color": ("7C3AED", "DB2777"), "icon": "🎨"},
    5: {"color": ("0369A1", "059669"), "icon": "💊"},
    6: {"color": ("0EA5E9", "6366F1"), "icon": "👁️"},
    7: {"color": ("F59E0B", "EF4444"), "icon": "✨"},
    8: {"color": ("10B981", "3B82F6"), "icon": "🔧"},
    9: {"color": ("EC4899", "8B5CF6"), "icon": "🏥"},
    10: {"color": ("64748B", "334155"), "icon": "💻"},
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
    6: {
        "title": "CLIP: Learning Transferable Visual Models From Natural Language",
        "summary": (
            "CLIP trains a vision encoder and text encoder jointly on 400M image-text pairs from the internet "
            "using contrastive learning, enabling zero-shot transfer to downstream vision tasks without "
            "task-specific fine-tuning. The model matches or exceeds supervised baselines on over 30 benchmarks "
            "including ImageNet, demonstrating the power of natural language supervision for visual learning."
        ),
        "contributions": [
            "Introduces contrastive language-image pretraining (CLIP) on 400M web-scraped image-text pairs",
            "Achieves zero-shot ImageNet accuracy of 76.2%, matching supervised ResNet-50",
            "Demonstrates strong transfer learning across 30+ vision benchmarks without fine-tuning",
            "Releases WIT (WebImageText) dataset of 400M image-text pairs",
            "Shows natural language is a flexible supervision signal for vision models",
        ],
        "reproducibility_score": 8.9,
        "code_availability": "HIGH",
        "datasets": "PARTIAL",
        "methodology_clarity": "VERY GOOD",
        "code_link": "https://github.com/openai/CLIP",
        "data_link": "N/A (WIT not publicly released)",
    },
    7: {
        "title": "Attention Is All You Need",
        "summary": (
            "This landmark paper introduces the Transformer architecture, which relies entirely on self-attention "
            "mechanisms and dispenses with recurrence and convolutions. The Transformer achieves state-of-the-art "
            "performance on English-to-German and English-to-French translation tasks while being significantly "
            "more parallelizable and requiring less training time than recurrent models."
        ),
        "contributions": [
            "Proposes the Transformer: first sequence model based solely on self-attention",
            "Introduces multi-head attention mechanism for parallel sequence processing",
            "Achieves 28.4 BLEU on WMT 2014 English-to-German, surpassing all previous models",
            "Reduces training time from weeks to 12 hours on 8 GPUs via full parallelization",
            "Establishes the foundation for BERT, GPT, and virtually all modern LLMs",
        ],
        "reproducibility_score": 9.5,
        "code_availability": "HIGH",
        "datasets": "OPEN",
        "methodology_clarity": "VERY GOOD",
        "code_link": "https://github.com/tensorflow/tensor2tensor",
        "data_link": "https://www.statmt.org/wmt14/",
    },
    8: {
        "title": "LoRA: Low-Rank Adaptation of Large Language Models",
        "summary": (
            "LoRA proposes a parameter-efficient fine-tuning method that freezes pretrained model weights and "
            "injects trainable low-rank decomposition matrices into each Transformer layer. This reduces the "
            "number of trainable parameters by 10,000x and GPU memory by 3x compared to full fine-tuning, "
            "while achieving comparable or better performance on downstream tasks."
        ),
        "contributions": [
            "Introduces LoRA: trainable rank decomposition matrices injected into frozen pretrained weights",
            "Reduces trainable parameters by 10,000x vs full fine-tuning on GPT-3 175B",
            "Matches or outperforms full fine-tuning on GLUE, SuperGLUE, and generation benchmarks",
            "No additional inference latency compared to adapter-based methods",
            "Releases open-source implementation compatible with HuggingFace transformers",
        ],
        "reproducibility_score": 9.2,
        "code_availability": "HIGH",
        "datasets": "OPEN",
        "methodology_clarity": "VERY GOOD",
        "code_link": "https://github.com/microsoft/LoRA",
        "data_link": "https://huggingface.co/datasets/glue",
    },
    9: {
        "title": "Segment Anything Model for Medical Image Segmentation",
        "summary": (
            "This paper adapts Meta's Segment Anything Model (SAM) to the medical imaging domain through "
            "domain-specific fine-tuning on diverse medical image datasets including CT, MRI, and endoscopy. "
            "The proposed MedSAM achieves superior zero-shot segmentation performance across 11 medical "
            "image modalities compared to general-purpose and task-specific segmentation models."
        ),
        "contributions": [
            "Adapts SAM foundation model for medical imaging via lightweight domain-specific fine-tuning",
            "Curates largest medical image segmentation dataset: 1.5M image-mask pairs across 11 modalities",
            "Achieves state-of-the-art on 11/14 medical segmentation benchmarks in zero-shot setting",
            "Demonstrates strong generalization to unseen medical imaging devices and protocols",
            "Releases MedSAM weights and training code under open-source license",
        ],
        "reproducibility_score": 8.4,
        "code_availability": "HIGH",
        "datasets": "PARTIAL",
        "methodology_clarity": "GOOD",
        "code_link": "https://github.com/bowang-lab/MedSAM",
        "data_link": "N/A (partially restricted)",
    },
    10: {
        "title": "Reinforcement Learning from Human Feedback for Code Generation",
        "summary": (
            "This paper applies RLHF to improve code generation quality beyond what supervised fine-tuning "
            "achieves. Human preference data is collected on code correctness, readability, and efficiency, "
            "then used to train a reward model that guides PPO-based policy optimization of a code LLM, "
            "resulting in significant improvements on HumanEval and CodeContests benchmarks."
        ),
        "contributions": [
            "First systematic application of RLHF to code generation with human preference annotations",
            "Improves HumanEval pass@1 by 14.2% over SFT baseline using PPO fine-tuning",
            "Introduces CodePref dataset: 50K human preference comparisons on code quality",
            "Shows RLHF improves code readability and efficiency beyond functional correctness",
            "Ablation study identifying reward model size as key factor for RLHF code gains",
        ],
        "reproducibility_score": 6.5,
        "code_availability": "LOW",
        "datasets": "CLOSED",
        "methodology_clarity": "FAIR",
        "code_link": "N/A",
        "data_link": "N/A (proprietary dataset)",
    },
}


def _clean(text: str) -> str:
    import re
    import html
    text = re.sub(r'<[^>]+>', '', str(text))
    return html.escape(text).strip()


def _make_panel_thumbnail(visual: dict, title: str = "", authors: str = "") -> str:
    c1, c2 = visual["color"]
    img_b64 = visual.get("thumbnail")
    if img_b64:
        return f"<img src='data:image/png;base64,{img_b64}' style='width:110px; min-width:110px; height:140px; object-fit:cover; object-position:top; border-radius:12px; box-shadow:0 4px 16px rgba(0,0,0,0.15);'/>"
    short_title = title[:80] + "..." if len(title) > 80 else title
    short_authors = authors[:40] + "..." if len(authors) > 40 else authors
    return f"""
    <div style='
        background:white; border:1px solid #E2E8F0;
        border-radius:12px; min-width:110px; width:110px; height:140px;
        overflow:hidden; box-shadow:0 4px 16px rgba(0,0,0,0.10);
        padding:10px;
        display:flex; flex-direction:column; justify-content:flex-start;
    '>
        <div style='font-size:7.5px; font-weight:700; color:#1E293B; line-height:1.5; margin-bottom:8px; word-break:break-word;'>{short_title}</div>
        <div style='height:1px; background:#E2E8F0; margin-bottom:6px;'></div>
        <div style='font-size:6px; color:#64748B; line-height:1.5;'>{short_authors}</div>
    </div>"""


def _render_analysis(analysis: dict, visual: dict):
    c1, c2 = visual["color"]
    title = analysis.get('title', '')
    authors = analysis.get('authors', '')
    thumb_html = _make_panel_thumbnail(visual, title, authors)

    # 헤더
    thumbnail_b64 = visual.get("thumbnail")
    thumb_col, info_col = st.columns([1, 2.5])

    with thumb_col:
        if thumbnail_b64:
            import base64
            st.image(base64.b64decode(thumbnail_b64), use_container_width=True)
        else:
            st.markdown(thumb_html, unsafe_allow_html=True)

    with info_col:
        st.markdown(f"""
        <div style='padding-top:4px;'>
          <div style='font-size:12px; color:#2563EB; font-weight:600; margin-bottom:6px;'>
            ✨ AI-Powered Paper Analysis
          </div>
          <div style='font-size:15px; font-weight:700; color:#1E293B; line-height:1.5; margin-bottom:12px;'>
            {_clean(analysis.get('title', ''))}
          </div>
          <div style='display:flex; gap:8px; flex-wrap:wrap;'>
            <span style='background:#EFF6FF; color:#2563EB; padding:3px 10px;
                         border-radius:12px; font-size:11px; font-weight:600;'>📄 PDF</span>
            <span style='background:#F0FDF4; color:#15803D; padding:3px 10px;
                         border-radius:12px; font-size:11px; font-weight:600;'>✅ 분석 완료</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    # 요약
    summary_text = _clean(analysis.get('summary', ''))
    summary_html = summary_text if summary_text else "<span style='color:#94A3B8;'>요약 정보가 없습니다.</span>"
    st.markdown(f"""
      <div class="section-card">
        <div class="section-title">📋 논문 요약</div>
        <div style='font-size:13px; color:#334155; line-height:1.7;'>{summary_html}</div>
      </div>
    """, unsafe_allow_html=True)

    # 핵심 기여 + 신뢰도 점수
    contrib_col, rely_col = st.columns([1.2, 1])

    with contrib_col:
        contributions_html = "".join(
            f"<li style='margin-bottom:6px; color:#334155; font-size:13px;'>{_clean(c)}</li>"
            for c in analysis.get("contributions", [])
        )
        st.markdown(f"""
        <div class="section-card">
          <div class="section-title">🔑 핵심 기여</div>
          <ul style='padding-left:16px; margin:0;'>
            {contributions_html}
          </ul>
        </div>
        """, unsafe_allow_html=True)

    with rely_col:
        # 새 구조: reliability.score / 구 구조: reproducibility_score
        if "reliability" in analysis:
            score = analysis["reliability"].get("score", "-")
            reason = analysis["reliability"].get("evaluation_reason", "")
            st.markdown(f"""
            <div class="section-card">
              <div class="section-title">⭐ 신뢰도 점수</div>
              <div style='text-align:center; padding:12px 0;'>
                <span style='font-size:42px; font-weight:800; color:#2563EB;'>{score}</span>
                <span style='font-size:18px; color:#94A3B8;'> / 100</span>
              </div>
              <div style='font-size:11px; color:#64748B; line-height:1.6;'>{reason[:200]}{'...' if len(reason) > 200 else ''}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            score = analysis.get("reproducibility_score", "-")
            st.markdown(f"""
            <div class="section-card">
              <div class="section-title">✅ 재현성 점수</div>
              <div style='text-align:center; padding:12px 0;'>
                <span style='font-size:42px; font-weight:800; color:#2563EB;'>{score}</span>
                <span style='font-size:18px; color:#94A3B8;'> / 10</span>
              </div>
              <div class="metric-row">
                <div class="metric-item">
                  <div class="metric-value">{analysis.get('code_availability', '-')}</div>
                  <div class="metric-label">CODE</div>
                </div>
                <div class="metric-item">
                  <div class="metric-value">{analysis.get('datasets', '-')}</div>
                  <div class="metric-label">DATASETS</div>
                </div>
                <div class="metric-item">
                  <div class="metric-value">{analysis.get('methodology_clarity', '-')}</div>
                  <div class="metric-label">CLARITY</div>
                </div>
              </div>
            </div>
            """, unsafe_allow_html=True)

    # 재현성 상세 (새 구조)
    if "reproducibility" in analysis:
        repro = analysis["reproducibility"]
        st.markdown(f"""
        <div class="section-card">
          <div class="section-title">🔬 재현성 분석</div>
          <div style='font-size:13px; color:#334155; line-height:1.8;'>
            <b>데이터셋:</b> {repro.get('dataset_status', '-')}<br/>
            <b>방법론 상세도:</b> {repro.get('method_detail_level', '-')[:200]}{'...' if len(repro.get('method_detail_level','')) > 200 else ''}<br/>
            <b>코드 공개:</b> {repro.get('code_availability', '-')}
          </div>
        </div>
        """, unsafe_allow_html=True)

    # 난이도 + 검색 키워드
    diff_col, query_col = st.columns([1, 1])

    with diff_col:
        if "difficulty" in analysis:
            diff = analysis["difficulty"]
            level = diff.get("level", "-")
            level_color = {"Beginner": "#15803D", "Intermediate": "#A16207", "Advanced": "#DC2626"}.get(level, "#64748B")
            knowledge_html = "".join(
                f"<span style='background:#F1F5F9; color:#475569; padding:2px 8px; border-radius:10px; font-size:11px; margin:2px; display:inline-block;'>{k}</span>"
                for k in diff.get("required_knowledge", [])
            )
            st.markdown(f"""
            <div class="section-card">
              <div class="section-title">📊 논문 난이도</div>
              <div style='text-align:center; margin-bottom:10px;'>
                <span style='background:{level_color}; color:white; padding:4px 16px;
                             border-radius:12px; font-size:14px; font-weight:700;'>{level}</span>
              </div>
              <div style='margin-bottom:6px; font-size:11px; color:#94A3B8;'>필요 배경지식</div>
              <div>{knowledge_html}</div>
            </div>
            """, unsafe_allow_html=True)

    with query_col:
        if "search_queries" in analysis:
            queries = analysis["search_queries"]
            queries_html = "".join(
                f"<div style='background:#EFF6FF; color:#2563EB; padding:5px 10px; border-radius:6px; font-size:12px; margin-bottom:6px;'>🔍 {q}</div>"
                for q in queries
            )
            st.markdown(f"""
            <div class="section-card">
              <div class="section-title">🔎 관련 검색어</div>
              {queries_html}
            </div>
            """, unsafe_allow_html=True)



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
                st.session_state.pdf_first_page = None
                st.rerun()

    # PDF 업로드 모드
    if st.session_state.selected_paper == "pdf":
        pdf_name = st.session_state.get("pdf_name", "업로드된 논문")
        pdf_text = st.session_state.get("pdf_text", "")
        pdf_analysis = st.session_state.get("pdf_analysis")

        if pdf_analysis and "error" not in pdf_analysis:
            img_b64 = st.session_state.get("pdf_first_page")
            visual = {"color": ("2563EB", "7C3AED"), "icon": "📄", "thumbnail": img_b64}
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

        if pdf_analysis and "error" in pdf_analysis:
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

import streamlit as st

# 임시 더미 데이터 (나중에 OpenAlex API로 교체)
DUMMY_PAPERS = [
    {
        "id": 1,
        "title": "Transformers for Large-Scale Text Classification: A Survey",
        "authors": "A. Sharma, J. Lee, et al.",
        "citations": 2456,
        "q_level": "Q1",
        "journal": "Computer Vision and Pattern Recognition",
        "year": 2023,
        "doi": "10.1234/example1",
    },
    {
        "id": 2,
        "title": "Self-Supervised Learning in Medical Imaging",
        "authors": "A. Sharma, A. Lee, et al.",
        "citations": 1120,
        "q_level": "Q2",
        "journal": "Medical Informatics",
        "year": 2022,
        "doi": "10.1234/example2",
    },
    {
        "id": 3,
        "title": "Efficient Neural Architecture Search for Edge Devices",
        "authors": "A. Sharma, J. Lee, et al.",
        "citations": 2456,
        "q_level": "Q2",
        "journal": "Computer Vision and AI Recognition",
        "year": 2023,
        "doi": "10.1234/example3",
    },
    {
        "id": 4,
        "title": "Diffusion Models for Image Synthesis: A Comprehensive Review",
        "authors": "B. Kim, C. Park, et al.",
        "citations": 3812,
        "q_level": "Q1",
        "journal": "Neural Information Processing Systems",
        "year": 2023,
        "doi": "10.1234/example4",
    },
    {
        "id": 5,
        "title": "Graph Neural Networks in Drug Discovery",
        "authors": "D. Choi, E. Jung, et al.",
        "citations": 987,
        "q_level": "Q3",
        "journal": "Bioinformatics",
        "year": 2022,
        "doi": "10.1234/example5",
    },
]

BADGE_CLASS = {"Q1": "badge-q1", "Q2": "badge-q2", "Q3": "badge-q3"}


def render_paper_list():
    st.markdown("""
    <div style='background:white; border-radius:12px; padding:18px 20px;
                box-shadow:0 2px 8px rgba(0,0,0,0.08);'>
      <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:14px;'>
        <span style='font-weight:700; font-size:16px; color:#1E293B;'>All papers</span>
        <span style='font-size:12px; color:#94A3B8;'>Page 1 of 3</span>
      </div>
    """, unsafe_allow_html=True)

    for paper in DUMMY_PAPERS:
        badge_cls = BADGE_CLASS.get(paper["q_level"], "badge-q2")
        is_selected = st.session_state.selected_paper == paper["id"]
        card_cls = "paper-card selected" if is_selected else "paper-card"

        st.markdown(f"""
        <div class="{card_cls}">
          <div class="paper-title">{paper['title']}</div>
          <div class="paper-authors">👥 {paper['authors']}</div>
          <div class="paper-meta">
            <span class="paper-citations">⭐ {paper['citations']:,} citations</span>
            <span>Journal Q-level</span>
            <span class="{badge_cls}">{paper['q_level']}</span>
            <span style="color:#64748B">- {paper['journal']}</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button(f"📊 AI 분석", key=f"analyze_{paper['id']}", use_container_width=True):
            st.session_state.selected_paper = paper["id"]
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

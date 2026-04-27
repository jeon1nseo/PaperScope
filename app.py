import streamlit as st
from components.paper_list import render_paper_list
from components.analysis_panel import render_analysis_panel

st.set_page_config(
    page_title="PaperScope",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
  /* 전체 배경 */
  .stApp { background-color: #F1F5F9; }

  /* 헤더 숨기기 */
  header[data-testid="stHeader"] { display: none; }

  /* 메인 패딩 제거 */
  .block-container { padding: 0 !important; max-width: 100% !important; }

  /* 상단 네비게이션 바 */
  .nav-bar {
    background: #1E293B;
    padding: 14px 24px;
    display: flex;
    align-items: center;
    gap: 16px;
    position: sticky;
    top: 0;
    z-index: 100;
  }
  .nav-logo {
    color: #38BDF8;
    font-size: 22px;
    font-weight: 800;
    letter-spacing: -0.5px;
  }
  .nav-search {
    flex: 1;
    max-width: 480px;
    background: #334155;
    border-radius: 8px;
    padding: 8px 14px;
    color: #94A3B8;
    font-size: 14px;
  }

  /* Q레벨 배지 */
  .badge-q1 {
    background: #DCFCE7; color: #15803D;
    padding: 2px 10px; border-radius: 12px; font-size: 12px; font-weight: 600;
  }
  .badge-q2 {
    background: #FEF9C3; color: #A16207;
    padding: 2px 10px; border-radius: 12px; font-size: 12px; font-weight: 600;
  }
  .badge-q3 {
    background: #FFEDD5; color: #C2410C;
    padding: 2px 10px; border-radius: 12px; font-size: 12px; font-weight: 600;
  }

  /* 논문 카드 */
  .paper-card {
    background: white;
    border-radius: 10px;
    padding: 16px 18px;
    margin-bottom: 10px;
    border: 2px solid transparent;
    cursor: pointer;
    transition: all 0.15s ease;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06);
  }
  .paper-card:hover { border-color: #93C5FD; box-shadow: 0 4px 12px rgba(37,99,235,0.1); }
  .paper-card.selected { border-color: #2563EB; box-shadow: 0 4px 16px rgba(37,99,235,0.15); }
  .paper-title { font-weight: 700; color: #1E293B; font-size: 14px; margin-bottom: 4px; }
  .paper-authors { color: #64748B; font-size: 12px; margin-bottom: 10px; }
  .paper-meta { display: flex; align-items: center; gap: 12px; font-size: 12px; }
  .paper-citations { color: #475569; }

  /* 분석 패널 */
  .analysis-panel {
    background: white;
    border-radius: 12px;
    padding: 24px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
  }
  .analysis-title { font-size: 18px; font-weight: 700; color: #1E293B; margin-bottom: 20px; }

  .section-card {
    background: #F8FAFC;
    border-radius: 8px;
    padding: 16px;
    margin-bottom: 14px;
    border: 1px solid #E2E8F0;
  }
  .section-title {
    font-size: 12px; font-weight: 700; color: #64748B;
    letter-spacing: 0.05em; text-transform: uppercase;
    margin-bottom: 10px;
    display: flex; align-items: center; gap: 6px;
  }

  /* 재현성 점수 */
  .repro-score {
    text-align: center;
    padding: 16px;
  }
  .score-number {
    font-size: 42px; font-weight: 800; color: #2563EB;
  }
  .score-max { font-size: 20px; color: #94A3B8; }
  .score-label { font-size: 12px; color: #94A3B8; margin-top: 4px; }

  .metric-row {
    display: flex; justify-content: space-between;
    margin-top: 14px;
  }
  .metric-item { text-align: center; }
  .metric-value { font-size: 12px; font-weight: 700; color: #1E293B; }
  .metric-label { font-size: 10px; color: #94A3B8; }

  /* 다운로드 버튼 */
  .dl-btn {
    background: #EFF6FF; color: #2563EB;
    border: 1px solid #BFDBFE;
    border-radius: 6px; padding: 5px 12px;
    font-size: 12px; font-weight: 600;
    text-decoration: none;
    display: inline-flex; align-items: center; gap: 4px;
  }
</style>
""", unsafe_allow_html=True)

# 상단 네비게이션 바
st.markdown("""
<div class="nav-bar">
  <div class="nav-logo">📄 PaperScope</div>
  <div class="nav-search">🔍 &nbsp; Search academic papers, topics, authors...</div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

# 세션 상태 초기화
if "selected_paper" not in st.session_state:
    st.session_state.selected_paper = None
if "pdf_text" not in st.session_state:
    st.session_state.pdf_text = ""
if "pdf_name" not in st.session_state:
    st.session_state.pdf_name = ""
if "pdf_analysis" not in st.session_state:
    st.session_state.pdf_analysis = None

# 두 패널 레이아웃
left_col, right_col = st.columns([1, 1.2], gap="medium")

with left_col:
    render_paper_list()

with right_col:
    render_analysis_panel()

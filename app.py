import streamlit as st
from components.paper_list import render_paper_list
from components.analysis_panel import render_analysis_panel
from components.auth import render_login, render_signup, render_forgot_password

st.set_page_config(
    page_title="PaperScope",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# 세션 상태 초기화
if "page" not in st.session_state:
    st.session_state.page = "login"
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_email" not in st.session_state:
    st.session_state.user_email = ""
if "user_nickname" not in st.session_state:
    st.session_state.user_nickname = ""
if "auth_error" not in st.session_state:
    st.session_state.auth_error = ""
if "auth_success" not in st.session_state:
    st.session_state.auth_success = ""
if "selected_paper" not in st.session_state:
    st.session_state.selected_paper = None
if "pdf_text" not in st.session_state:
    st.session_state.pdf_text = ""
if "pdf_name" not in st.session_state:
    st.session_state.pdf_name = ""
if "pdf_analysis" not in st.session_state:
    st.session_state.pdf_analysis = None

# ── 인증 페이지 ──────────────────────────────────────
if not st.session_state.logged_in:
    st.markdown("""
    <style>
      .stApp { background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%); }
      header[data-testid="stHeader"] { display: none; }
      .block-container { padding: 2rem 1rem !important; max-width: 100% !important; }
      div[data-testid="stTextInput"] input {
        border-radius: 10px !important;
        border: 1.5px solid #E2E8F0 !important;
        padding: 10px 14px !important;
        font-size: 14px !important;
        background-color: white !important;
        color: #1E293B !important;
      }
      div[data-testid="stTextInput"] input:focus {
        border-color: #2563EB !important;
        box-shadow: 0 0 0 3px rgba(37,99,235,0.1) !important;
        background-color: white !important;
      }
      div[data-testid="stTextInput"] label {
        color: white !important;
      }
      .stButton > button {
        border-radius: 10px !important;
        font-weight: 600 !important;
        padding: 10px !important;
      }
      .error-msg {
        background: #FEF2F2; border: 1px solid #FECACA;
        color: #DC2626; border-radius: 8px;
        padding: 10px 14px; font-size: 13px; margin-bottom: 12px;
      }
      .success-msg {
        background: #F0FDF4; border: 1px solid #BBF7D0;
        color: #15803D; border-radius: 8px;
        padding: 10px 14px; font-size: 13px; margin-bottom: 12px;
      }
    </style>
    """, unsafe_allow_html=True)

    if st.session_state.page == "login":
        render_login()
    elif st.session_state.page == "signup":
        render_signup()
    elif st.session_state.page == "forgot_password":
        render_forgot_password()
    st.stop()

# ── 메인 앱 (로그인 후) ──────────────────────────────
st.markdown("""
<style>
  .stApp { background-color: #F1F5F9; }
  header[data-testid="stHeader"] { display: none; }
  .block-container { padding: 0 !important; max-width: 100% !important; }

  .nav-bar {
    background: #1E293B;
    padding: 14px 24px;
    display: flex;
    align-items: center;
    gap: 16px;
  }
  .nav-logo { color: #38BDF8; font-size: 22px; font-weight: 800; letter-spacing: -0.5px; }

  .badge-q1 { background: #DCFCE7; color: #15803D; padding: 2px 10px; border-radius: 12px; font-size: 12px; font-weight: 600; }
  .badge-q2 { background: #FEF9C3; color: #A16207; padding: 2px 10px; border-radius: 12px; font-size: 12px; font-weight: 600; }
  .badge-q3 { background: #FFEDD5; color: #C2410C; padding: 2px 10px; border-radius: 12px; font-size: 12px; font-weight: 600; }

  .paper-card {
    background: white; border-radius: 10px; padding: 16px 18px;
    margin-bottom: 10px; border: 2px solid transparent;
    cursor: pointer; transition: all 0.15s ease;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06);
  }
  .paper-card:hover { border-color: #93C5FD; box-shadow: 0 4px 12px rgba(37,99,235,0.1); }
  .paper-card.selected { border-color: #2563EB; box-shadow: 0 4px 16px rgba(37,99,235,0.15); }
  .paper-title { font-weight: 700; color: #1E293B; font-size: 14px; margin-bottom: 4px; }
  .paper-authors { color: #64748B; font-size: 12px; margin-bottom: 10px; }
  .paper-meta { display: flex; align-items: center; gap: 12px; font-size: 12px; }
  .paper-citations { color: #475569; }

  .section-card {
    background: #F8FAFC; border-radius: 8px; padding: 16px;
    margin-bottom: 14px; border: 1px solid #E2E8F0;
  }
  .section-title {
    font-size: 12px; font-weight: 700; color: #64748B;
    letter-spacing: 0.05em; text-transform: uppercase;
    margin-bottom: 10px;
  }
  .repro-score { text-align: center; padding: 16px; }
  .score-number { font-size: 42px; font-weight: 800; color: #2563EB; }
  .score-max { font-size: 20px; color: #94A3B8; }
  .score-label { font-size: 12px; color: #94A3B8; margin-top: 4px; }
  .metric-row { display: flex; justify-content: space-between; margin-top: 14px; }
  .metric-item { text-align: center; }
  .metric-value { font-size: 12px; font-weight: 700; color: #1E293B; }
  .metric-label { font-size: 10px; color: #94A3B8; }
</style>
""", unsafe_allow_html=True)

# 상단 네비게이션 바
nav_col, user_col = st.columns([6, 1])
with nav_col:
    st.markdown("""
    <div class="nav-bar">
      <div class="nav-logo">📄 PaperScope</div>
    </div>
    """, unsafe_allow_html=True)
with user_col:
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    nickname = st.session_state.user_nickname
    if st.button(f"👤 {nickname}  |  로그아웃", key="logout"):
        st.session_state.logged_in = False
        st.session_state.page = "login"
        st.session_state.user_email = ""
        st.session_state.user_nickname = ""
        st.rerun()

st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

# 두 패널 레이아웃
left_col, right_col = st.columns([1, 1.2], gap="medium")

with left_col:
    render_paper_list()

with right_col:
    render_analysis_panel()

import streamlit as st

AUTH_CSS = """
<style>
  .auth-wrapper {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, #0F172A 0%, #1E293B 50%, #0F172A 100%);
  }
  .auth-card {
    background: white;
    border-radius: 20px;
    padding: 48px 40px;
    width: 100%;
    max-width: 440px;
    box-shadow: 0 25px 50px rgba(0,0,0,0.3);
  }
  .auth-logo {
    text-align: center;
    margin-bottom: 8px;
  }
  .auth-logo-text {
    font-size: 28px;
    font-weight: 800;
    color: #1E293B;
    letter-spacing: -0.5px;
  }
  .auth-logo-dot {
    color: #2563EB;
  }
  .auth-subtitle {
    text-align: center;
    color: #94A3B8;
    font-size: 14px;
    margin-bottom: 32px;
  }
  .auth-divider {
    display: flex;
    align-items: center;
    gap: 12px;
    margin: 20px 0;
    color: #CBD5E1;
    font-size: 13px;
  }
  .auth-divider-line {
    flex: 1;
    height: 1px;
    background: #E2E8F0;
  }
  .sns-btn {
    width: 100%;
    padding: 11px 16px;
    border-radius: 10px;
    border: 1.5px solid #E2E8F0;
    background: white;
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    margin-bottom: 10px;
    transition: all 0.15s;
    color: #1E293B;
  }
  .sns-btn:hover { background: #F8FAFC; border-color: #CBD5E1; }
  .sns-kakao { border-color: #FEE500; background: #FEE500; color: #191919; }
  .sns-kakao:hover { background: #F0D900; }
  .sns-naver { border-color: #03C75A; background: #03C75A; color: white; }
  .sns-naver:hover { background: #02B350; }
  .sns-google { border-color: #E2E8F0; }
  .auth-footer {
    text-align: center;
    margin-top: 24px;
    font-size: 14px;
    color: #64748B;
  }
  .auth-link {
    color: #2563EB;
    font-weight: 600;
    cursor: pointer;
    text-decoration: none;
  }
  .input-label {
    font-size: 13px;
    font-weight: 600;
    color: #374151;
    margin-bottom: 4px;
  }
  .error-msg {
    background: #FEF2F2;
    border: 1px solid #FECACA;
    color: #DC2626;
    border-radius: 8px;
    padding: 10px 14px;
    font-size: 13px;
    margin-bottom: 12px;
  }
  .success-msg {
    background: #F0FDF4;
    border: 1px solid #BBF7D0;
    color: #15803D;
    border-radius: 8px;
    padding: 10px 14px;
    font-size: 13px;
    margin-bottom: 12px;
  }
</style>
"""


def render_login():
    st.markdown(AUTH_CSS, unsafe_allow_html=True)

    _, center, _ = st.columns([1, 1.2, 1])

    with center:
        st.markdown("""
        <div style='text-align:center; margin-bottom:8px;'>
          <span style='font-size:32px; font-weight:800; color:white;'>
            📄 Paper<span style='color:#38BDF8;'>Scope</span>
          </span>
        </div>
        <div style='text-align:center; color:#94A3B8; font-size:14px; margin-bottom:32px;'>
          AI 기반 학술 논문 분석 서비스
        </div>
        """, unsafe_allow_html=True)

        # SNS 로그인
        g_col, n_col, k_col = st.columns(3)
        with g_col:
            if st.button("🌐  Google", use_container_width=True, key="google_login"):
                st.toast("Google 로그인은 준비 중입니다.")
        with n_col:
            if st.button("🟢  Naver", use_container_width=True, key="naver_login"):
                st.toast("Naver 로그인은 준비 중입니다.")
        with k_col:
            if st.button("🟡  Kakao", use_container_width=True, key="kakao_login"):
                st.toast("Kakao 로그인은 준비 중입니다.")

        st.markdown("""
        <div style='display:flex; align-items:center; gap:12px; margin:20px 0; color:#94A3B8; font-size:13px;'>
          <div style='flex:1; height:1px; background:#E2E8F0;'></div>
          또는 이메일로 로그인
          <div style='flex:1; height:1px; background:#E2E8F0;'></div>
        </div>
        """, unsafe_allow_html=True)

        # 에러 메시지
        if st.session_state.get("auth_error"):
            st.markdown(f"""
            <div class='error-msg'>⚠️ {st.session_state.auth_error}</div>
            """, unsafe_allow_html=True)
            st.session_state.auth_error = ""

        email = st.text_input("이메일", placeholder="example@email.com", key="login_email")
        password = st.text_input("비밀번호", type="password", placeholder="비밀번호 입력", key="login_pw")

        st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

        if st.button("로그인", use_container_width=True, type="primary", key="login_submit"):
            if not email or not password:
                st.session_state.auth_error = "이메일과 비밀번호를 입력해주세요."
                st.rerun()
            else:
                # 임시: 아무 이메일/비밀번호나 허용 (추후 Firebase 연동)
                st.session_state.logged_in = True
                st.session_state.user_email = email
                st.session_state.user_nickname = email.split("@")[0]
                st.session_state.page = "main"
                st.rerun()

        forgot_col, _ = st.columns([1, 2])
        with forgot_col:
            if st.button("비밀번호 찾기", key="forgot_pw"):
                st.session_state.page = "forgot_password"
                st.rerun()

        st.markdown("""
        <div style='text-align:center; margin-top:24px; font-size:14px; color:#64748B;'>
          계정이 없으신가요?
        </div>
        """, unsafe_allow_html=True)

        if st.button("회원가입", use_container_width=True, key="go_signup"):
            st.session_state.page = "signup"
            st.rerun()


def render_signup():
    st.markdown(AUTH_CSS, unsafe_allow_html=True)

    _, center, _ = st.columns([1, 1.2, 1])

    with center:
        st.markdown("""
        <div style='text-align:center; margin-bottom:8px;'>
          <span style='font-size:28px; font-weight:800; color:#1E293B;'>
            📄 Paper<span style='color:#2563EB;'>Scope</span>
          </span>
        </div>
        <div style='text-align:center; color:#94A3B8; font-size:14px; margin-bottom:28px;'>
          회원가입
        </div>
        """, unsafe_allow_html=True)

        if st.session_state.get("auth_error"):
            st.markdown(f"<div class='error-msg'>⚠️ {st.session_state.auth_error}</div>",
                        unsafe_allow_html=True)
            st.session_state.auth_error = ""

        email = st.text_input("이메일 *", placeholder="example@email.com", key="signup_email")
        password = st.text_input("비밀번호 *", type="password", placeholder="8자 이상 입력", key="signup_pw")
        password2 = st.text_input("비밀번호 확인 *", type="password", placeholder="비밀번호 재입력", key="signup_pw2")
        nickname = st.text_input("닉네임 *", placeholder="사용할 닉네임 입력", key="signup_nickname")

        col1, col2 = st.columns(2)
        with col1:
            birth = st.text_input("생년월일", placeholder="YYYYMMDD", key="signup_birth")
        with col2:
            gender = st.selectbox("성별", ["선택 안 함", "남성", "여성"], key="signup_gender")

        st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

        if st.button("가입하기", use_container_width=True, type="primary", key="signup_submit"):
            if not email or not password or not password2 or not nickname:
                st.session_state.auth_error = "필수 항목(*)을 모두 입력해주세요."
                st.rerun()
            elif password != password2:
                st.session_state.auth_error = "비밀번호가 일치하지 않습니다."
                st.rerun()
            elif len(password) < 8:
                st.session_state.auth_error = "비밀번호는 8자 이상이어야 합니다."
                st.rerun()
            else:
                # 임시: 바로 로그인 처리 (추후 Firebase 연동)
                st.session_state.logged_in = True
                st.session_state.user_email = email
                st.session_state.user_nickname = nickname
                st.session_state.page = "main"
                st.rerun()

        st.markdown("""
        <div style='text-align:center; margin-top:16px; font-size:14px; color:#64748B;'>
          이미 계정이 있으신가요?
        </div>
        """, unsafe_allow_html=True)

        if st.button("로그인으로 돌아가기", use_container_width=True, key="go_login"):
            st.session_state.page = "login"
            st.rerun()


def render_forgot_password():
    st.markdown(AUTH_CSS, unsafe_allow_html=True)

    _, center, _ = st.columns([1, 1.2, 1])

    with center:
        st.markdown("""
        <div style='text-align:center; margin-bottom:8px;'>
          <span style='font-size:28px; font-weight:800; color:#1E293B;'>
            🔑 비밀번호 찾기
          </span>
        </div>
        <div style='text-align:center; color:#94A3B8; font-size:14px; margin-bottom:28px;'>
          가입한 이메일로 초기화 링크를 보내드립니다
        </div>
        """, unsafe_allow_html=True)

        if st.session_state.get("auth_success"):
            st.markdown(f"<div class='success-msg'>✅ {st.session_state.auth_success}</div>",
                        unsafe_allow_html=True)
            st.session_state.auth_success = ""

        email = st.text_input("가입한 이메일", placeholder="example@email.com", key="forgot_email")

        if st.button("초기화 링크 발송", use_container_width=True, type="primary", key="forgot_submit"):
            if not email:
                st.session_state.auth_error = "이메일을 입력해주세요."
                st.rerun()
            else:
                # 임시: 성공 메시지 표시 (추후 SMTP 연동)
                st.session_state.auth_success = f"{email} 로 초기화 링크를 발송했습니다."
                st.rerun()

        if st.button("로그인으로 돌아가기", use_container_width=True, key="back_to_login"):
            st.session_state.page = "login"
            st.rerun()

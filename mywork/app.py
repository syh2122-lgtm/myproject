import streamlit as st
import sqlite3
import datetime

st.set_page_config(layout="wide", page_title="국어과 AIDT")

# 1. DB 초기화 함수 (테이블 생성)
def init_db():
    conn = sqlite3.connect('myproject.db')
    c = conn.cursor()
    # users 테이블 생성
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            userid TEXT UNIQUE,
            password TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    # learning_history 테이블 생성
    c.execute('''
        CREATE TABLE IF NOT EXISTS learning_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            userid TEXT,
            m1 INTEGER, m2 INTEGER, m3 INTEGER, m4 INTEGER, m5 INTEGER,
            m6 INTEGER, m7 INTEGER, m8 INTEGER, m9 INTEGER, m10 INTEGER,
            score INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# 세션 상태 초기화 (로그인 유지용)
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
    st.session_state['userid'] = ""

init_db()

# 2. 사이드바: 로그인 및 회원가입 시스템
with st.sidebar:
    if not st.session_state['logged_in']:
        st.subheader("로그인 / 회원가입")
        choice = st.radio("선택해주세요", ["로그인", "회원가입"])
        
        if choice == "회원가입":
            with st.form("signup_form"):
                new_user = st.text_input("아이디 (userid)")
                new_password = st.text_input("비밀번호", type='password')
                submit_signup = st.form_submit_button("가입하기")
                
                if submit_signup:
                    if new_user and new_password:
                        try:
                            conn = sqlite3.connect('myproject.db')
                            c = conn.cursor()
                            c.execute("INSERT INTO users (userid, password) VALUES (?, ?)", (new_user, new_password))
                            conn.commit()
                            conn.close()
                            st.success("회원가입 성공! 로그인해주세요.")
                        except sqlite3.IntegrityError:
                            st.error("이미 존재하는 아이디입니다.")
                    else:
                        st.warning("아이디와 비밀번호를 모두 입력하세요.")
                        
        elif choice == "로그인":
            with st.form("login_form"):
                log_user = st.text_input("아이디")
                log_password = st.text_input("비밀번호", type='password')
                submit_login = st.form_submit_button("로그인")
                
                if submit_login:
                    conn = sqlite3.connect('myproject.db')
                    c = conn.cursor()
                    c.execute("SELECT * FROM users WHERE userid=? AND password=?", (log_user, log_password))
                    result = c.fetchone()
                    conn.close()
                    
                    if result:
                        st.session_state['logged_in'] = True
                        st.session_state['userid'] = log_user
                        st.success(f"{log_user}님 환영합니다!")
                        st.rerun()
                    else:
                        st.error("아이디나 비밀번호가 틀렸습니다.")
    else:
        st.write(f"👤 **{st.session_state['userid']}**님 로그인 중")
        if st.button("로그아웃"):
            st.session_state['logged_in'] = False
            st.session_state['userid'] = ""
            st.rerun()

# 3. 메인 콘텐츠 (로그인 성공 시 혹은 기본 화면으로 노출)
if st.session_state['logged_in']:
    st.title('This is my first webapp!!')
    st.subheader('국어과 AIDT')
    
    coll1, coll2 = st.columns((4, 1))
    
    with coll1:
        with st.expander('2차시_ 동영상', expanded=False):
            st.title('동영상 시청......')
            # 경로 주의: 윈도우 환경에서는 백슬래시(\) 대신 슬래시(/) 사용을 권장합니다.
            imgpath1 = 'img/images1.png'
            try:
                st.image(imgpath1)
            except:
                st.warning("이미지 파일을 찾을 수 없습니다. 경로를 확인해주세요.")
                
        with st.expander('3차시_ 동영상', expanded=True):
            st.title('동영상 시청......')
            st.markdown("""
            ### **머신러닝(Machine Learning)이란?**
            * **정의:** 인공지능(AI)의 한 분야로, 컴퓨터가 명시적인 프로그래밍 없이 데이터로부터 스스로 학습하는 기술입니다.
            * **작동 원리:** 수많은 데이터를 분석하여 숨겨진 패턴과 규칙을 찾아내고, 이를 바탕으로 새로운 데이터에 대한 예측이나 결정을 수행합니다.
            * **주요 특징:** 
                * **데이터 의존성:** 양질의 데이터가 많을수록 성능이 향상됩니다.
                * **자기 학습:** 경험(데이터)을 통해 모델 스스로 지속적인 성능 개선이 가능합니다.
            """)
    
    with coll2:
        with st.expander('Tips...', expanded=True):
            st.subheader('Tips...')
            imgpath = 'https://i.ytimg.com/vi/MP8R6kBykzE/hqdefault.jpg'
            st.image(imgpath)
            st.write('This is a term....')
            st.markdown("""
            **💡 ML의 3가지 하위 개념**
            
            * **지도학습 (Supervised):** 
              정답(Label)이 있는 데이터로 학습합니다. (예: 분류, 회귀)
            * **비지도학습 (Unsupervised):** 
              정답이 없는 데이터에서 패턴을 찾습니다. (예: 군집화)
            * **강화학습 (Reinforcement):** 
              행동에 따른 보상을 통해 최적의 행동을 학습합니다.
            """)
else:
    st.info("👈 왼쪽 사이드바에서 로그인을 먼저 진행해 주세요.")
import streamlit as st
import sqlite3
import pandas as pd

# 1. 관리자 권한 확인 로직 (가장 먼저 실행되어야 함)
# 로그인이 안 되어 있거나, 로그인한 아이디가 '1234'가 아니면 접근을 차단합니다.
if 'logged_in' not in st.session_state or not st.session_state['logged_in'] or st.session_state.get('userid') != '1234':
    st.error("🚫 관리자 전용 페이지입니다. 학생들은 접근할 수 없습니다.")
    st.info("메인 화면에서 관리자 계정(아이디: 1234)으로 로그인해 주세요.")
    st.stop() # 이 코드가 실행되면 아래에 있는 데이터베이스 확인 코드는 아예 실행되지 않습니다.

# 2. 관리자(1234)로 로그인한 경우에만 아래 내용이 화면에 나타납니다.
st.title("🗄️ 데이터베이스(DB) 확인")

st.write(f"현재 접속 계정: **{st.session_state['userid']}**")
st.divider()

# users 테이블 데이터 불러오기
st.subheader("1. 가입된 회원 목록 (users 테이블)")
try:
    conn = sqlite3.connect('myproject.db')
    df_users = pd.read_sql_query("SELECT * FROM users", conn)
    st.dataframe(df_users, use_container_width=True)
except Exception as e:
    st.error(f"users 테이블을 불러오는 중 오류 발생: {e}")

# learning_history 테이블 데이터 불러오기
st.subheader("2. 형성평가 응시 기록 (learning_history 테이블)")
try:
    df_history = pd.read_sql_query("SELECT * FROM learning_history", conn)
    st.dataframe(df_history, use_container_width=True)
except Exception as e:
    st.error(f"learning_history 테이블을 불러오는 중 오류 발생: {e}")
finally:
    conn.close()
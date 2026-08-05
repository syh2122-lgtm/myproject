import streamlit as st
import streamlit.components.v1 as components
import os

# 페이지 기본 설정
st.set_page_config(page_title="머신러닝 문제 해결 사례", page_icon="🔍", layout="wide")

st.title("🔍 머신러닝 문제 해결 사례")
st.markdown("선생님이 직접 개발한 머신러닝 문제 해결 사례와 시뮬레이션을 아래에서 확인해 보세요!")
st.divider()

# 1. html 폴더 안에 있는 파일의 경로를 설정합니다. 
html_file_path = html_file_path = "html/example_case.html"
try:
    # 2. HTML 파일을 읽기 모드로 엽니다. (한글 깨짐 방지를 위해 utf-8 인코딩 사용)
    with open(html_file_path, 'r', encoding='utf-8') as f:
        html_source_code = f.read()
    
    # 3. Streamlit components를 이용해 iframe 형태로 렌더링합니다.
    # width 1024, height 768 적용 및 내용이 넘칠 경우 스크롤 허용
    with st.container():
        components.html(
            html_source_code,
            width=1024,
            height=768,
            scrolling=True
        )
        
except FileNotFoundError:
    # 파일 경로가 잘못되었거나 파일이 없을 때 나타나는 에러 메시지
    st.error(f"⚠️ '{html_file_path}' 파일을 찾을 수 없습니다.")
    st.info("app.py가 있는 위치에 'html' 폴더가 만들어져 있고, 그 안에 HTML 파일이 정확한 이름으로 들어있는지 확인해 주세요.")
except Exception as e:
    st.error(f"HTML 파일을 불러오는 중 오류가 발생했습니다: {e}")
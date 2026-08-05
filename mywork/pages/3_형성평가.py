import streamlit as st
import sqlite3

# 로그인 확인
if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    st.warning("로그인이 필요한 페이지입니다. 홈 화면에서 로그인해주세요.")
    st.stop()

st.title("📝 머신러닝 개념 형성평가")
st.write(f"👤 응시자: **{st.session_state['userid']}**님")
st.divider()

# 앞서 작성했던 10문제 리스트 (생략 없이 여기에 그대로 들어갑니다)
questions = [
    {"question": "머신러닝(기계학습)의 가장 올바른 정의는 무엇일까요?", "options": ["컴퓨터가 규칙대로 동작하는 것", "스스로 패턴을 찾는 기술", "자아를 가지는 기술", "배터리 수명 연장", "통신망 속도 증가"], "answer": 1},
    {"question": "정답을 미리 컴퓨터에 알려주고 학습시키는 방식은?", "options": ["지도 학습", "비지도 학습", "강화 학습", "자기주도 학습", "연합 학습"], "answer": 0},
    {"question": "정답 없이 비슷한 것끼리 그룹을 나누는 학습은?", "options": ["지도 학습", "비지도 학습", "강화 학습", "전이 학습", "반복 학습"], "answer": 1},
    {"question": "보상과 벌점을 통해 최선의 수를 학습하는 방식은?", "options": ["지도 학습", "비지도 학습", "강화 학습", "혼합 학습", "규칙 학습"], "answer": 2},
    {"question": "스팸 메일인지 정상 메일인지 구분하는 문제는?", "options": ["회귀", "분류", "군집화", "차원 축소", "시계열"], "answer": 1},
    {"question": "연속적인 수치를 예측하는 회귀(Regression) 문제로 적합한 것은?", "options": ["비 올지 예측", "암 판별", "사과/배 구분", "시험 점수 예측", "그룹 나누기"], "answer": 3},
    {"question": "데이터를 학습용과 평가용으로 나누는 이유는?", "options": ["용량 부족", "시간 단축", "새로운 데이터 예측 실력 확인", "데이터 오류", "수집 비용 아끼기"], "answer": 2},
    {"question": "노이즈까지 암기하여 새로운 데이터를 예측하지 못하는 현상은?", "options": ["과대적합", "과소적합", "정규화", "최적화", "일반화"], "answer": 0},
    {"question": "데이터의 개별 속성(평수, 거리 등)을 의미하는 용어는?", "options": ["라벨", "피처(Feature)", "파라미터", "알고리즘", "에포크"], "answer": 1},
    {"question": "인공지능, 머신러닝, 딥러닝의 포함 관계는?", "options": ["머신러닝 > 인공지능 > 딥러닝", "딥러닝 > 머신러닝 > 인공지능", "인공지능 > 딥러닝 > 머신러닝", "인공지능 > 머신러닝 > 딥러닝", "머신러닝 > 딥러닝 > 인공지능"], "answer": 3}
]

# Form을 사용하여 제출 버튼 클릭 시 한 번에 처리
with st.form("quiz_form"):
    user_answers = []
    
    for i, q in enumerate(questions):
        st.markdown(f"**Q{i+1}. {q['question']}**")
        ans = st.radio(f"q{i}", q['options'], key=f"q{i}", index=None, label_visibility="collapsed")
        user_answers.append(ans)
        st.write("")
        
    submit_button = st.form_submit_button("최종 제출 및 채점하기")

if submit_button:
    # 1. 채점 로직 (문항당 10점, 미응답은 틀린 것으로 간주)
    score = 0
    answer_indices = []
    
    for i, q in enumerate(questions):
        if user_answers[i] is not None:
            ans_idx = q['options'].index(user_answers[i])
            answer_indices.append(ans_idx)
            if ans_idx == q['answer']:
                score += 10
        else:
            answer_indices.append(-1) # 미응답 처리
            
    st.success(f"채점 완료! 총점: **{score} / 100 점**")

    # 2. DB 저장 로직 (학습 이력 기록)
    try:
        conn = sqlite3.connect('myproject.db')
        c = conn.cursor()
        
        # answer_indices 리스트를 언패킹하여 쿼리에 매핑
        query = '''
            INSERT INTO learning_history 
            (userid, m1, m2, m3, m4, m5, m6, m7, m8, m9, m10, score) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        data_tuple = (st.session_state['userid'], *answer_indices, score)
        
        c.execute(query, data_tuple)
        conn.commit()
        conn.close()
        st.info("✅ 평가 결과가 데이터베이스에 성공적으로 저장되었습니다.")
        
    except Exception as e:
        st.error(f"DB 저장 중 오류가 발생했습니다: {e}")
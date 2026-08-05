# streamlit webapp의 pages 경로 및에 서브 페이지로 다음을 생성해주세요.
# 머신러닝의 개념에 대해 학습할 콘텐츠 생성
# 간단하게 머신러닝의 개념을 실습할수 있는 시뮬레이터 포함(mock data를 생성해서(분류 데이터) 직접 실습하도록 함)

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# 한글 폰트 설정 (Mac, Windows, Linux 환경에 맞게 적용)
plt.rcParams['font.family'] = 'Malgun Gothic'   
# plt.rc('font', family='Malgun Gothic') # Windows용
plt.rcParams['axes.unicode_minus'] = False # 마이너스 기호 깨짐 방지

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="머신러닝의 개념",
    page_icon="🤖",
    layout="wide"
)

# 2. 머신러닝 개념 설명 섹션
st.title("🤖 머신러닝(Machine Learning)이란?")

st.markdown("""
### 📌 개념 이해하기
**머신러닝(기계 학습)**은 인공지능(AI)의 한 분야로, 컴퓨터가 명시적인 프로그래밍 없이 **데이터로부터 스스로 패턴을 학습**하여 새로운 데이터에 대한 결과를 예측하거나 결정하는 기술입니다.

#### 기존 프로그래밍 vs 머신러닝
*   💻 **기존 프로그래밍 (Rule-based):** 사람이 직접 규칙(Rule)과 데이터(Data)를 컴퓨터에 입력하면, 컴퓨터가 해답(Answers)을 출력합니다.
*   🧠 **머신러닝 (Machine Learning):** 데이터(Data)와 해답(Answers)을 컴퓨터에 주면, 컴퓨터가 스스로 학습하여 **규칙(Rules)**을 찾아냅니다.

---
""")

# 3. 실습 시뮬레이터 섹션
st.header("🛠️ 머신러닝 분류(Classification) 시뮬레이터")
st.markdown("""
머신러닝에서 가장 대표적인 작업 중 하나인 **분류(Classification)**를 직접 실습해 봅시다. 
아래 슬라이더를 조절하여 가상의 데이터를 생성하고, 인공지능 모델이 파란색 점과 빨간색 점을 어떻게 구분하는지 확인해 보세요.
""")

st.write("---")

# 레이아웃 나누기 (사이드바 또는 컬럼 활용)
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("⚙️ 데이터 및 모델 설정")
    
    # 사용자 입력: 데이터 포인트 수
    n_samples = st.slider("데이터 개수 (샘플 수)", min_value=100, max_value=1000, value=300, step=50)
    
    # 사용자 입력: 노이즈 (클래스가 섞이는 정도)
    noise_level = st.slider("데이터 혼잡도 (노이즈)", min_value=0.1, max_value=2.0, value=0.5, step=0.1)
    
    # 모델 학습 버튼
    train_button = st.button("🚀 인공지능 모델 학습시키기", type="primary")
    
    st.info("👈 설정값을 바꾼 후 버튼을 눌러 결과가 어떻게 달라지는지 확인해 보세요!")

# 데이터 생성 함수 (make_classification 활용)
@st.cache_data
def generate_mock_data(n_samples, noise_level):
    X, y = make_classification(
        n_samples=n_samples, 
        n_features=2, 
        n_redundant=0, 
        n_informative=2,
        random_state=42, 
        n_clusters_per_class=1, 
        class_sep=1.5 / noise_level # 노이즈가 클수록 클래스가 겹침
    )
    return X, y

# 결정 경계 시각화 함수
def plot_decision_boundary(X, y, model, ax):
    # 그리드 포인트 생성
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.05),
                         np.arange(y_min, y_max, 0.05))
    
    # 예측 수행
    if model is not None:
        Z = model.predict(np.c_[xx.ravel(), yy.ravel()])
        Z = Z.reshape(xx.shape)
        # 등고선 그리기 (결정 경계 배경)
        ax.contourf(xx, yy, Z, alpha=0.3, cmap=plt.cm.RdYlBu)
    
    # 산점도 그리기 (실제 데이터)
    scatter = ax.scatter(X[:, 0], X[:, 1], c=y, cmap=plt.cm.RdYlBu, edgecolor='k', alpha=0.8)
    
    ax.set_xlabel('특성 1 (Feature 1)')
    ax.set_ylabel('특성 2 (Feature 2)')
    return ax

with col2:
    # 1. 데이터 생성
    X, y = generate_mock_data(n_samples, noise_level)
    
    if not train_button:
        # 학습 전 데이터만 보여주기
        st.subheader("📊 생성된 가상 데이터")
        fig, ax = plt.subplots(figsize=(8, 6))
        plot_decision_boundary(X, y, None, ax)
        ax.set_title("학습 전 데이터 (분류 기준이 없음)")
        st.pyplot(fig)
        
    else:
        # 학습 후 결과 보여주기
        st.subheader("✨ 모델 학습 완료 및 예측 결과")
        
        # 데이터 분할 (학습용 / 테스트용)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # 머신러닝 모델 생성 및 학습 (랜덤 포레스트 사용)
        with st.spinner('모델이 데이터를 학습하고 있습니다...'):
            model = RandomForestClassifier(random_state=42)
            model.fit(X_train, y_train)
            
            # 예측 및 평가
            y_pred = model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            
        # 정확도 출력
        st.success(f"🎉 모델 학습 완료! **예측 정확도: {accuracy * 100:.1f}%**")
        
        # 시각화 (결정 경계)
        fig, ax = plt.subplots(figsize=(8, 6))
        plot_decision_boundary(X, y, model, ax)
        ax.set_title("학습된 인공지능의 분류 기준 (결정 경계)")
        st.pyplot(fig)
        
        st.markdown("""
        **💡 시각화 설명:**
        * 배경의 **빨간색 영역**과 **파란색 영역**은 인공지능 모델이 스스로 학습하여 그어놓은 '분류 기준선(결정 경계)'입니다.
        * 데이터가 섞여 있을수록(노이즈가 높을수록) 완벽하게 분류하기 어려워 정확도가 떨어지는 것을 볼 수 있습니다.
        """)
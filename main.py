# main.py (루트에 위치)
import streamlit as st
from pathlib import Path
import sys

# app 경로 추가 (중복 방지)
APP_DIR = Path(__file__).resolve().parent / "app"
if str(APP_DIR) not in sys.path:
    sys.path.append(str(APP_DIR))

# 앱 기본 설정
st.set_page_config(page_title="JudgFy", layout="wide")

# 사이드바 구성
st.sidebar.title("🧠 JudgFy 메뉴")
st.sidebar.markdown("왼쪽 사이드바에서 기능을 선택하세요.\n\n예: 판단 기록하기, 저장 보기 등")

# 본문 안내
st.markdown("## 🎯 환영합니다!")
st.markdown("JudgFy는 판단 흐름을 기록하고, 나중에 복기할 수 있도록 도와주는 도구입니다.\n\n왼쪽 메뉴에서 기능을 선택해 시작하세요.")


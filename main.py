# main.py (루트에 위치)
import streamlit as st
from pathlib import Path
import sys

# app/pages 경로 추가
APP_DIR = Path(__file__).resolve().parent / "app"
sys.path.append(str(APP_DIR))

# Streamlit 앱 구성
st.set_page_config(page_title="JudgFy", layout="wide")

st.sidebar.title("🧠 JudgFy 메뉴")
st.sidebar.markdown("왼쪽 메뉴에서 기능을 선택하세요.")

st.write("왼쪽 메뉴에서 기능을 선택하면 해당 기능 화면이 나타납니다.")
 

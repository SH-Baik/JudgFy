from pathlib import Path
import streamlit as st
import json
from utils.recording_module import extract_decision_elements

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "judgments.json"

st.title("💡 JudgFy - 판단 기록 & 추론")

user_input = st.text_area("💬 판단 상황을 자연스럽게 입력하세요:", height=150)

if st.button("💾 판단 구조화 및 저장"):
    if user_input.strip():
        result = extract_decision_elements(user_input)

        if "error" in result:
            st.error("❌ GPT 판단 구조화 중 오류 발생!")
            st.json(result)
        else:
            if DATA_PATH.exists():
                with open(DATA_PATH, "r", encoding="utf-8") as f:
                    try:
                        history = json.load(f)
                        st.write("불러온 타입:", type(history))  # ✅ 타입 확인
                        if not isinstance(history, list):
                            history = []
                    except json.JSONDecodeError:
                        history = []
            else:
                history = []

            history.append(result)

            with open(DATA_PATH, "w", encoding="utf-8") as f:
                json.dump(history, f, ensure_ascii=False, indent=2)

            st.success("✅ 판단이 저장되었습니다!")
            st.json(result)

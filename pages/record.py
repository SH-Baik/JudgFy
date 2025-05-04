import streamlit as st
import json
from modules.recording_module import extract_decision_elements
from pathlib import Path

DATA_PATH = Path("data/judgments.json")

st.title("💡 JudgFy - 판단 기록 & 추론")

# 입력 받기
user_input = st.text_area("💬 판단 상황을 자연스럽게 입력하세요:", height=150)

if st.button("💾 판단 구조화 및 저장"):
    if user_input.strip():
        result = extract_decision_elements(user_input)

        # 오류 처리
        if "error" in result:
            st.error("❌ GPT 판단 구조화 중 오류 발생!")
            st.json(result)
        else:
            # 기존 기록 불러오기
            if DATA_PATH.exists():
                with open(DATA_PATH, "r", encoding="utf-8") as f:
                    try:
                        history = json.load(f)
                        if not isinstance(history, list):
                            history = []
                    except json.JSONDecodeError:
                        history = []
            else:
                history = []

            # 기록 추가 및 저장
            history.append(result)
            with open(DATA_PATH, "w", encoding="utf-8") as f:
                json.dump(history, f, ensure_ascii=False, indent=2)

            st.success("✅ 판단이 저장되었습니다!")
            st.json(result)
    else:
        st.warning("입력 내용이 없습니다. 판단 상황을 입력해주세요.")

# 판단 기록 보기
st.markdown("---")
st.markdown("📂 **저장된 판단 기록**")

if DATA_PATH.exists():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        try:
            history = json.load(f)
            if not isinstance(history, list):
                history = []
        except json.JSONDecodeError:
            history = []
else:
    history = []

if history:
    for i, record in enumerate(reversed(history[-5:]), 1):
        st.markdown(f"**{i}️⃣ 상황:** {record.get('situation', '')}")
        st.markdown(f"🧠 **판단:** {record.get('decision', '')}")
        st.markdown(f"📌 **기준:** {', '.join(record.get('criteria', []))}")
        st.markdown("---")
else:
    st.info("저장된 판단 기록이 없습니다.")


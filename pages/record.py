import streamlit as st
import json
from pathlib import Path
from modules.recording_module import extract_decision_elements

DATA_PATH = Path("data/judgments.json")

st.title("💡 JudgFy - 판단 기록 & 추론")

# 입력
user_input = st.text_area("💬 판단 상황을 자연스럽게 입력하세요:", height=150)

# 판단 구조화 및 저장
if st.button("💾 판단 구조화 및 저장"):
    if user_input.strip():
        result = extract_decision_elements(user_input)

        # GPT 처리 중 오류 발생 시
        if "error" in result:
            st.error("❌ GPT 판단 구조화 중 오류 발생!")
            st.json(result)
        else:
            # 데이터 파일 존재 여부 확인 및 안전 로딩
            if DATA_PATH.exists():
                try:
                    with open(DATA_PATH, "r", encoding="utf-8") as f:
                        history = json.load(f)
                        if not isinstance(history, list):  # 방어 코드
                            history = []
                except json.JSONDecodeError:
                    history = []
            else:
                history = []

            # 판단 결과 추가
            history.append(result)

            # 파일에 저장
            with open(DATA_PATH, "w", encoding="utf-8") as f:
                json.dump(history, f, ensure_ascii=False, indent=2)

            st.success("✅ 판단이 저장되었습니다!")
            st.json(result)
    else:
        st.warning("입력이 비어 있습니다. 내용을 작성해주세요.")

# 판단 기록 보기
st.markdown("---")
st.markdown("📂 **저장된 판단 기록**")

if DATA_PATH.exists():
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            history = json.load(f)
            if not isinstance(history, list):  # 방어 코드
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

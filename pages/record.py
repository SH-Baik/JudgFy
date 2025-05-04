import streamlit as st
import json
from pathlib import Path
from utils.recording_module import extract_decision_elements  # ✅ 경로 수정

# ✅ 절대경로로 안전하게 처리
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "judgments.json"

st.title("💡 JudgFy - 판단 기록 & 추론")

# 사용자 입력
user_input = st.text_area("💬 판단 상황을 자연스럽게 입력하세요:", height=150)

if st.button("💾 판단 구조화 및 저장"):
    if user_input.strip():
        result = extract_decision_elements(user_input)

        if "error" in result:
            st.error("❌ GPT 판단 구조화 중 오류 발생!")
            st.json(result)
        else:
            # ✅ JSON 파일 불러오기
            if DATA_PATH.exists():
                try:
                    with open(DATA_PATH, "r", encoding="utf-8") as f:
                        history = json.load(f)
                        if not isinstance(history, list):
                            st.warning("⚠️ history가 list가 아닙니다. 초기화합니다.")
                            history = []
                except json.JSONDecodeError:
                    history = []
            else:
                history = []

            # ✅ append 하기 전에도 list인지 확인
            if isinstance(history, list):
                history.append(result)
                with open(DATA_PATH, "w", encoding="utf-8") as f:
                    json.dump(history, f, ensure_ascii=False, indent=2)
                st.success("✅ 판단이 저장되었습니다!")
                st.json(result)
            else:
                st.error("❌ 판단 기록 저장 실패: 내부 구조가 비정상입니다.")

# 판단 기록 보기
st.markdown("---")
st.markdown("📂 **저장된 판단 기록**")

if DATA_PATH.exists():
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            history = json.load(f)
            if not isinstance(history, list):
                history = []
    except json.JSONDecodeError:
        history = []
else:
    history = []

# ✅ 최근 5개 판단 출력
if isinstance(history, list) and history:
    for i, record in enumerate(reversed(history[-5:]), 1):
        st.markdown(f"**{i}️⃣ 상황:** {record.get('situation', '')}")
        st.markdown(f"🧠 **판단:** {record.get('decision', '')}")
        st.markdown(f"📌 **기준:** {', '.join(record.get('criteria', []))}")
        st.markdown("---")
else:
    st.info("저장된 판단 기록이 없습니다.")

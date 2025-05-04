import streamlit as st
import json
from pathlib import Path
from app.modules.recording_module import extract_decision_elements  # 경로 확인 필요

# 절대 경로 지정
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "judgments.json"

st.title("💡 JudgFy - 판단 기록 & 추론")

# 사용자 입력 받기
user_input = st.text_area("💬 판단 상황을 자연스럽게 입력하세요:", height=150)

if st.button("💾 판단 구조화 및 저장"):
    if user_input.strip():
        result = extract_decision_elements(user_input)

        if "error" in result:
            st.error("❌ GPT 판단 구조화 중 오류 발생!")
            st.json(result)
        else:
            # 판단 기록 파일 불러오기
            if DATA_PATH.exists():
                try:
                    with open(DATA_PATH, "r", encoding="utf-8") as f:
                        history = json.load(f)
                        if not isinstance(history, list):
                            st.warning("⚠️ history가 list가 아님. 초기화합니다.")
                            history = []
                except json.JSONDecodeError:
                    st.error("❌ JSON 파싱 실패. history 초기화함")
                    history = []
            else:
                history = []

            # 판단 기록 저장
            if isinstance(history, list):
                history.append(result)
                with open(DATA_PATH, "w", encoding="utf-8") as f:
                    json.dump(history, f, ensure_ascii=False, indent=2)
                st.success("✅ 판단이 저장되었습니다!")
                st.json(result)
            else:
                st.error("❌ 판단 기록 저장 실패: 내부 구조가 비정상입니다.")

# 판단 기록 출력
st.markdown("---")
st.markdown("📂 **저장된 판단 기록**")

st.write("📌 [디버그] 파일 경로:", str(DATA_PATH))

if DATA_PATH.exists():
    st.write("✅ [디버그] 파일 존재함")
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            history = json.load(f)
            st.write("📌 [디버그] JSON 로딩 성공")
            st.write("📌 [디버그] 타입:", str(type(history)))
            st.write("📌 [디버그] 내용:", history)
            if not isinstance(history, list):
                st.warning("⚠️ 기록 구조가 리스트가 아님. 초기화합니다.")
                history = []
    except json.JSONDecodeError:
        st.error("❌ JSON 파싱 오류")
        history = []
else:
    st.warning("❗ 판단 기록 파일이 존재하지 않습니다.")
    history = []

if isinstance(history, list) and history:
    for i, record in enumerate(reversed(history[-5:]), 1):
        if isinstance(record, dict):
            st.markdown(f"**{i}️⃣ 상황:** {record.get('situation', '')}")
            st.markdown(f"🧠 **판단:** {record.get('decision', '')}")
            st.markdown(f"📌 **기준:** {', '.join(record.get('criteria', []))}")
            st.markdown("---")
        else:
            st.warning(f"⚠️ 잘못된 판단 기록이 감지되었습니다: {record}")
else:
    st.info("저장된 판단 기록이 없습니다.")

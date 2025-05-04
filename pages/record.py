import streamlit as st
import json
from pathlib import Path
from app.modules.recording_module import extract_decision_elements  # ← 경로 맞게 조정

# 절대경로로 파일 지정
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "judgments.json"

st.title("💡 JudgFy - 판단 기록 & 추론")
user_input = st.text_area("💬 판단 상황을 자연스럽게 입력하세요:", height=150)

# 🔒 판단 저장
if st.button("💾 판단 구조화 및 저장"):
    if user_input.strip():
        result = extract_decision_elements(user_input)

        if "error" in result:
            st.error("❌ GPT 판단 구조화 중 오류 발생!")
            st.json(result)
        else:
            # 판단 기록 불러오기
            if DATA_PATH.exists():
                try:
                    with open(DATA_PATH, "r", encoding="utf-8") as f:
                        history = json.load(f)
                        if not isinstance(history, list):
                            st.warning("⚠️ 저장 파일이 리스트가 아닙니다. 빈 리스트로 초기화합니다.")
                            history = []
                except json.JSONDecodeError:
                    st.warning("⚠️ JSON 파싱 오류 발생. 빈 리스트로 초기화합니다.")
                    history = []
            else:
                history = []

            # 리스트일 경우에만 append
            if isinstance(history, list):
                history.append(result)
                with open(DATA_PATH, "w", encoding="utf-8") as f:
                    json.dump(history, f, ensure_ascii=False, indent=2)
                st.success("✅ 판단이 저장되었습니다!")
                st.json(result)
            else:
                st.error("❌ 판단 기록 저장 실패: history가 리스트가 아님")

# 🔍 판단 기록 보기
st.markdown("---")
st.subheader("📂 저장된 판단 기록")

# history 불러오기
if DATA_PATH.exists():
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            history = json.load(f)
            if not isinstance(history, list):
                st.warning("⚠️ history가 리스트가 아닙니다. 표시를 생략합니다.")
                history = []
    except json.JSONDecodeError:
        st.warning("⚠️ JSON 파싱 오류")
        history = []
else:
    history = []

# 디버깅 정보 출력 (선택)
st.caption(f"📊 [디버깅] 현재 history 타입: `{type(history)}`")

# 최근 5개 출력
if isinstance(history, list) and history:
    for i, record in enumerate(reversed(history[-5:]), 1):
        st.markdown(f"**{i}️⃣ 상황:** {record.get('situation', '')}")
        st.markdown(f"🧠 **판단:** {record.get('decision', '')}")
        st.markdown(f"📌 **기준:** {', '.join(record.get('criteria', []))}")
        st.markdown("---")
else:
    st.info("저장된 판단 기록이 없습니다.")

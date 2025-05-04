import streamlit as st
import json
from pathlib import Path
from app.modules.recording_module import extract_decision_elements  # 필요시 경로 조정

# ✅ 경로 설정
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "judgments.json"

st.title("💡 JudgFy - 판단 기록 & 추론")

# ✅ 디버깅용: 현재 경로 및 파일 상태 확인
st.caption(f"📂 데이터 경로: `{DATA_PATH}`")
if DATA_PATH.exists():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        try:
            debug_content = json.load(f)
            st.caption(f"📄 데이터 타입: {type(debug_content).__name__}")
        except Exception as e:
            st.caption(f"⚠️ 로드 실패: {e}")

# ✅ 사용자 입력
user_input = st.text_area("💬 판단 상황을 자연스럽게 입력하세요:", height=150)

if st.button("💾 판단 구조화 및 저장"):
    if user_input.strip():
        result = extract_decision_elements(user_input)

        if "error" in result:
            st.error("❌ GPT 판단 구조화 중 오류 발생!")
            st.json(result)
        else:
            # 기록 불러오기
            if DATA_PATH.exists():
                try:
                    with open(DATA_PATH, "r", encoding="utf-8") as f:
                        history = json.load(f)
                        if not isinstance(history, list):
                            st.warning("⚠️ 기록이 리스트 형식이 아닙니다. 새로 초기화합니다.")
                            history = []
                except json.JSONDecodeError:
                    st.warning("⚠️ JSON 디코딩 실패. 새로 초기화합니다.")
                    history = []
            else:
                history = []

            # 저장
            history.append(result)
            with open(DATA_PATH, "w", encoding="utf-8") as f:
                json.dump(history, f, ensure_ascii=False, indent=2)

            st.success("✅ 판단이 저장되었습니다!")
            st.json(result)
    else:
        st.warning("⚠️ 입력 내용을 작성해 주세요.")

# ✅ 판단 기록 출력
st.markdown("---")
st.markdown("📂 **저장된 판단 기록**")

if DATA_PATH.exists():
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            history = json.load(f)
            if not isinstance(history, list):
                st.warning("⚠️ 기록 형식이 올바르지 않아 초기화합니다.")
                history = []
    except json.JSONDecodeError:
        st.warning("⚠️ JSON 파싱 오류로 인해 기록을 불러올 수 없습니다.")
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

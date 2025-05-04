import streamlit as st
import json
from pathlib import Path
from app.modules.recording_module import extract_decision_elements  # ✅ GPT 구조화 함수

# ✅ 안전한 경로 설정
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "judgments.json"

st.title("💡 JudgFy - 판단 기록 & 추론")

# 사용자 입력창
user_input = st.text_area("💬 판단 상황을 자연스럽게 입력하세요:", height=150)

# GPT 구조화 + 저장 버튼
if st.button("💾 판단 구조화 및 저장"):
    if user_input.strip():
        result = extract_decision_elements(user_input)

        if "error" in result:
            st.error("❌ GPT 판단 구조화 중 오류 발생!")
            st.json(result)
        else:
            # ✅ 기존 판단 기록 불러오기
            if DATA_PATH.exists():
                try:
                    with open(DATA_PATH, "r", encoding="utf-8") as f:
                        content = f.read()
                        print("🔍 파일 내용:", content)
                        f.seek(0)
                        history = json.load(f)
                        print("✅ 로드된 타입:", type(history))
                        if not isinstance(history, list):
                            print("⚠️ history가 list가 아닙니다. 초기화합니다.")
                            history = []
                except json.JSONDecodeError:
                    print("❌ JSONDecodeError 발생 → 초기화")
                    history = []
            else:
                history = []

            # ✅ 판단 기록 추가 및 저장
            if isinstance(history, list):
                history.append(result)
                with open(DATA_PATH, "w", encoding="utf-8") as f:
                    json.dump(history, f, ensure_ascii=False, indent=2)
                st.success("✅ 판단이 저장되었습니다!")
                st.json(result)
            else:
                st.error("❌ 판단 기록 저장 실패: 내부 구조가 비정상입니다.")

# ----------------------------------------
# ✅ 판단 기록 출력
st.markdown("---")
st.markdown("📂 **저장된 판단 기록**")

# 다시 로드 (중복 있지만 안전성 확보 목적)
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

# ✅ 최근 5개 판단 보여주기
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


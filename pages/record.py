import streamlit as st
import json
from pathlib import Path
import sys

# ✅ 모듈 경로 설정 (프로젝트 루트 기준으로 app/modules 접근 가능하게)
sys.path.append(str(Path(__file__).resolve().parents[1] / "app"))

# ✅ 판단 구조화 모듈 import
from modules.recording_module import extract_decision_elements

# ✅ 데이터 저장 경로
DATA_PATH = Path("data/judgments.json")

st.title("💡 JudgFy - 판단 기록 & 추론")

# ✅ 사용자 입력
user_input = st.text_area("💬 판단 상황을 자연스럽게 입력하세요:", height=150)

# ✅ 판단 구조화 및 저장
if st.button("💾 판단 구조화 및 저장"):
    if user_input.strip():
        result = extract_decision_elements(user_input)

        if "error" in result:
            st.error("❌ GPT 판단 구조화 중 오류 발생!")
            st.json(result)
        else:
            # 기존 파일 불러오기 (없거나 형식 문제 시 빈 리스트로 초기화)
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

            history.append(result)

            with open(DATA_PATH, "w", encoding="utf-8") as f:
                json.dump(history, f, ensure_ascii=False, indent=2)

            st.success("✅ 판단이 저장되었습니다!")
            st.json(result)

# ✅ 판단 기록 보기
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

    if history:
        for i, record in enumerate(reversed(history[-5:]), 1):
            st.markdown(f"**{i}️⃣ 상황:** {record.get('situation', '')}")
            st.markdown(f"🧠 **판단:** {record.get('decision', '')}")
            st.markdown(f"📌 **기준:** {', '.join(record.get('criteria', []))}")
            st.markdown("---")
    else:
        st.info("저장된 판단 기록이 없습니다.")
else:
    st.info("아직 판단이 저장되지 않았습니다.")

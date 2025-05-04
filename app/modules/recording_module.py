import openai
import os
import json
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# 현재 API Key 출력 (디버깅용)
print("🔑 현재 API Key:", openai.api_key)

def extract_decision_elements(text):
    """
    사용자가 입력한 판단 상황을 구조화된 JSON으로 반환하는 함수
    반환 구조:
    {
        "situation": "...",
        "options": ["...", "..."],
        "criteria": ["...", "..."],
        "decision": "...",
        "reflection": "..."
    }
    """
    prompt = f"""
다음 사용자가 입력한 상황을 다음 구조로 정리해주세요:

- situation: 상황 요약
- options: 고려한 선택지 목록
- criteria: 판단 기준
- decision: 최종 판단
- reflection: 나중에 돌아봤을 때 느낀 점 (예측)

입력:
\"\"\"{text}\"\"\"

출력은 반드시 JSON 형식으로 주세요.
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",  # 또는 "gpt-3.5-turbo"
            messages=[
                {"role": "system", "content": "당신은 사용자의 판단을 구조화해주는 분석가입니다."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        content = response["choices"][0]["message"]["content"]

        # 안전한 JSON 파싱 시도
        result = json.loads(content)
        return result

    except Exception as e:
        # 오류가 발생한 경우에도 내용 추적
        return {
            "error": str(e),
            "raw": content if 'content' in locals() else "No content"
        }

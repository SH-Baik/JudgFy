import openai
import os
import json
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# 디버깅용 출력
print("🔑 현재 API Key:", openai.api_key)

MODEL = "gpt-4o"  # 또는 "gpt-3.5-turbo"

def extract_decision_elements(text):
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
            model=MODEL,
            messages=[
                {"role": "system", "content": "당신은 사용자의 판단을 구조화해주는 분석가입니다."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )

        choices = response.get("choices", [])
        if choices and "message" in choices[0] and "content" in choices[0]["message"]:
            content = choices[0]["message"]["content"]
        else:
            return {"error": "Invalid response structure", "raw": str(response)}

        try:
            result = json.loads(content)
            return result
        except json.JSONDecodeError as je:
            return {"error": f"JSONDecodeError: {str(je)}", "raw": content}

    except Exception as e:
        return {
            "error": str(e),
            "raw": content if 'content' in locals() else "No content"
        }


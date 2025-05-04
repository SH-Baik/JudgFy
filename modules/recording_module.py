import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def extract_decision_elements(text):
    prompt = f"""
다음 사용자 입력 판단 상황을 다음 구조로 정리해줘:
- situation: 상황 요약
- options: 고려한 선택지 목록
- criteria: 판단 기준
- decision: 최종 판단
- reflection: 나중에 돌아봤을 때 느낀 점 (예측)

입력:
{text}

출력은 JSON 형식으로.
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )
    content = response['choices'][0]['message']['content']
try:
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    content = response['choices'][0]['message']['content']
    import json
    result = json.loads(content)
except Exception as e:
    result = {"error": str(e)}

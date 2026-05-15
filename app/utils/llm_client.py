import os

from dotenv import load_dotenv
from openai import OpenAI

# .env を読み込む
load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

client = OpenAI(api_key=API_KEY)

def call_llm(prompt: str) -> str:
    """
    LLM を最小コストで呼び出す関数。
    gpt-4o-mini を使うので開発中の費用はほぼゼロ。
    """
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2  # 低めにして安定性を優先
    )

    return response.choices[0].message.content

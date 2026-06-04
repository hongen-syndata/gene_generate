import json
import os

from app.schemas.panel import Panel
from app.utils.llm_client import call_llm


def load_prompt():
    base_dir = os.path.dirname(__file__)  # app/services/
    prompt_path = os.path.join(base_dir, "..", "prompts", "panel_prompt.txt")
    prompt_path = os.path.abspath(prompt_path)

    with open(prompt_path, encoding="utf-8") as f:
        return f.read()


def render_prompt(template: str, disease_name: str) -> str:
    return template.replace("{{disease}}", disease_name)


def clean_json(text: str) -> str:
    text = text.strip()

    # 先頭が ``` で始まる場合
    if text.startswith("```"):
        # ```json または ``` の行を削除
        lines = text.split("\n")
        # 最初の行（```json）を除去
        lines = lines[1:]
        # 最後の行（```）を除去
        if lines[-1].strip().startswith("```"):
            lines = lines[:-1]
        text = "\n".join(lines)

    return text.strip()


def generate_panel(disease_name: str) -> Panel:
    template = load_prompt()
    prompt = render_prompt(template, disease_name)

    llm_output = call_llm(prompt)
    cleaned = clean_json(llm_output)

    try:
        data = json.loads(cleaned)
        return Panel(**data)
    except json.JSONDecodeError:
        # 1回だけリトライ
        llm_output = call_llm(prompt)
        cleaned = clean_json(llm_output)
        data = json.loads(cleaned)
        return Panel(**data)

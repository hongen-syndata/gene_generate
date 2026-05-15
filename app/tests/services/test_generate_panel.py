# tests/test_panel.py
from app.schemas.panel import Panel
from app.services.generate_panel import clean_json, generate_panel, render_prompt


def test_clean_json_removes_codeblock():
    raw = """```json
{
  "disease": "Test",
  "generated_at": "2025-01-01",
  "genes": []
}
```"""
    cleaned = clean_json(raw)
    assert cleaned.startswith("{")
    assert cleaned.endswith("}")

def test_render_prompt():
    template = "Disease: {{disease}}"
    result = render_prompt(template, "Cancer")
    assert result == "Disease: Cancer"

def test_generate_panel_success(mocker):
    # モックする LLM 出力
    mock_json = """
    {
      "disease": "Cancer",
      "generated_at": "2025-01-01",
      "genes": []
    }
    """

    mocker.patch("app.services.generate_panel.call_llm", return_value=mock_json)

    panel = generate_panel("Cancer")

    assert isinstance(panel, Panel)
    assert panel.disease == "Cancer"
    assert panel.genes == []

def test_generate_panel_retry(mocker):
    # 1回目は壊れた JSON → 2回目で成功
    broken = "INVALID_JSON"
    valid = """
    {
      "disease": "Cancer",
      "generated_at": "2025-01-01",
      "genes": []
    }
    """

    mocker.patch(
        "app.services.generate_panel.call_llm",
        side_effect=[broken, valid]
    )

    panel = generate_panel("Cancer")

    assert isinstance(panel, Panel)
    assert panel.disease == "Cancer"

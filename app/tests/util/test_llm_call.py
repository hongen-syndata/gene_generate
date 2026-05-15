# tests/test_llm_client.py
from app.utils.llm_client import call_llm


def test_call_llm(mocker):
    # --- モックの戻り値を作る ---
    mock_response = mocker.Mock()
    mock_choice = mocker.Mock()
    mock_message = mocker.Mock()

    mock_message.content = "mocked response"
    mock_choice.message = mock_message
    mock_response.choices = [mock_choice]

    # --- create() をモック ---
    mock_create = mocker.patch(
        "app.utils.llm_client.client.chat.completions.create",
        return_value=mock_response
    )

    # --- 実行 ---
    result = call_llm("Hello")

    # --- 検証 ---
    assert result == "mocked response"

    # create が正しい引数で呼ばれたか確認
    mock_create.assert_called_once()
    args, kwargs = mock_create.call_args

    assert kwargs["model"] is not None
    assert kwargs["messages"][1]["content"] == "Hello"

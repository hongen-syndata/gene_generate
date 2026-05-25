from app.utils.llm_client import call_llm


def test_call_llm(mocker):
    # --- モックの戻り値を作る ---
    mock_response = mocker.Mock()
    mock_choice = mocker.Mock()
    mock_message = mocker.Mock()

    mock_message.content = "mocked response"
    mock_choice.message = mock_message
    mock_response.choices = [mock_choice]

    # --- OpenAI クライアントをモック ---
    mock_client = mocker.Mock()
    mock_client.chat.completions.create.return_value = mock_response

    mock_openai = mocker.patch("app.utils.llm_client.OpenAI", return_value=mock_client)

    # --- 実行 ---
    result = call_llm("hello")

    # --- 検証 ---
    assert result == "mocked response"
    mock_openai.assert_called_once()
    mock_client.chat.completions.create.assert_called_once()

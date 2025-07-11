import pytest
from unittest.mock import patch, MagicMock
import time

# Dynamically import agent module and class
import app.llm_agent as llm_mod

AgentClass = next(
    (
        getattr(llm_mod, name)
        for name in dir(llm_mod)
        if isinstance(getattr(llm_mod, name), type)
        and hasattr(getattr(llm_mod, name), "chat")
    ),
    None,
)
if AgentClass is None:
    pytest.skip("No chat-capable class in app.llm_agent", allow_module_level=True)


@patch("openai.ChatCompletion.create")
def test_retry_exhaustion_calls_n_plus_one(mock_create):
    # Always throw exception
    mock_create.side_effect = Exception("fail")
    max_retries = 2
    agent = AgentClass(api_key="key", model="m", max_retries=max_retries)
    with pytest.raises(Exception):
        agent.chat("msg")
    # initial call + retries
    assert mock_create.call_count == max_retries + 1


@patch("openai.ChatCompletion.create")
def test_unexpected_response_formats_raise_value_error(mock_create):
    # Case: missing 'choices'
    mock_create.return_value = {}
    agent = AgentClass(api_key="key", model="m")
    with pytest.raises(ValueError):
        agent.chat("msg")

    # Case: empty choices list
    mock_create.return_value = {"choices": []}
    with pytest.raises(ValueError):
        agent.chat("msg")


@patch("openai.ChatCompletion.create")
def test_streaming_response_assembly(mock_create):
    # Simulate streaming chunks
    chunks = [
        MagicMock(choices=[MagicMock(delta={"content": "Hel"})]),
        MagicMock(choices=[MagicMock(delta={"content": "lo"})]),
        MagicMock(choices=[MagicMock(delta={})]),
        MagicMock(choices=[MagicMock(delta={"content": "!"})]),
    ]
    mock_create.return_value = (c for c in chunks)
    agent = AgentClass(api_key="key", model="m", stream=True)
    result = agent.chat("test")
    assert result == "Hello!"


@patch("openai.ChatCompletion.create")
def test_batching_invokes_chat_multiple_times(mock_create):
    # Simulate simple non-streaming response
    mock_create.return_value = {"choices": [{"message": {"content": "OK"}}]}
    agent = AgentClass(api_key="key", model="m")
    prompts = ["a", "b", "c"]
    # batch size 2 -> two batches: ['a','b'], ['c']
    results = agent.chat_batch(prompts, batch_size=2)
    assert results == ["OK", "OK", "OK"]
    assert mock_create.call_count == 3


@patch("openai.ChatCompletion.create")
def test_backoff_delay(mock_create, monkeypatch):
    # Ensure exponential backoff delays are applied
    # First two calls fail, third succeeds
    mock_create.side_effect = [
        Exception(),
        Exception(),
        {"choices": [{"message": {"content": "Done"}}]},
    ]
    sleeps = []
    monkeypatch.setattr(time, "sleep", lambda s: sleeps.append(s))
    agent = AgentClass(api_key="key", model="m", max_retries=2, backoff_factor=0.1)
    result = agent.chat("prompt")
    assert result == "Done"
    # Expected backoffs: 0.1 * 2**0 = 0.1, 0.1 * 2**1 = 0.2
    assert sleeps == [0.1, 0.2]

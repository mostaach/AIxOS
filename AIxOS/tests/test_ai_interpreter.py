import pytest
from unittest.mock import MagicMock, patch
from aixos.core.config import AppConfig
from aixos.core.ai_interpreter import AIInterpreter

@pytest.fixture
def config():
    """Fixture for AppConfig."""
    return AppConfig(
        ai_model_api_key="fake-api-key",
        ai_model_name="gpt-3.5-turbo"
    )

@pytest.fixture
def interpreter(config):
    """Fixture for AIInterpreter."""
    return AIInterpreter(config)

class TestAIInterpreterPatternMatching:
    """Test cases for pattern matching in AIInterpreter."""

    def test_install_pattern(self, interpreter):
        """Test matching for install commands."""
        result = interpreter.try_pattern_matching("install python and git")
        assert result is not None
        assert len(result['commands']) == 2
        assert result['commands'][0]['description'] == 'Install python'
        assert result['commands'][1]['description'] == 'Install git'
        assert 'install' in result['commands'][0]['type']

    def test_create_folder_pattern(self, interpreter):
        """Test matching for create folder commands."""
        result = interpreter.try_pattern_matching("create a new folder called my_project")
        assert result is not None
        assert len(result['commands']) == 1
        assert result['commands'][0]['command'] == 'mkdir -p my_project'
        assert 'create' in result['commands'][0]['type']

    def test_list_files_pattern(self, interpreter):
        """Test matching for list files commands."""
        result = interpreter.try_pattern_matching("show me the files in this directory")
        assert result is not None
        assert len(result['commands']) == 1
        assert result['commands'][0]['command'] == 'ls -la'
        assert 'list' in result['commands'][0]['type']

    def test_update_system_pattern(self, interpreter):
        """Test matching for update system commands."""
        result = interpreter.try_pattern_matching("update all system packages")
        assert result is not None
        assert len(result['commands']) == 1
        assert 'update' in result['commands'][0]['type']

    def test_no_match(self, interpreter):
        """Test that no match returns None."""
        result = interpreter.try_pattern_matching("a very obscure command")
        assert result is None


@patch('aixos.core.ai_interpreter.openai')
class TestAIInterpreterAIInterpretation:
    """Test cases for AI-based interpretation."""

    def test_ai_interpret_success(self, mock_openai, interpreter):
        """Test successful AI interpretation with valid JSON response."""
        mock_response = MagicMock()
        mock_response.choices[0].message.content = '{"intent": "test intent", "commands": [{"command": "echo test", "description": "test command", "type": "test"}], "confidence": 0.9}'
        mock_openai.ChatCompletion.create.return_value = mock_response

        result = interpreter.ai_interpret("some command")
        assert result['intent'] == 'test intent'
        assert result['method'] == 'ai_interpretation'
        assert len(result['commands']) == 1
        mock_openai.ChatCompletion.create.assert_called_once()

    def test_ai_interpret_json_decode_error(self, mock_openai, interpreter):
        """Test AI interpretation with an invalid JSON response."""
        mock_response = MagicMock()
        mock_response.choices[0].message.content = 'this is not json'
        mock_openai.ChatCompletion.create.return_value = mock_response

        result = interpreter.ai_interpret("some command")
        assert result['intent'] == 'AI interpretation failed - using fallback'
        assert result['method'] == 'ai_interpretation_failed'
        assert 'raw_response' in result

    def test_ai_interpret_api_error(self, mock_openai, interpreter):
        """Test AI interpretation when the API call fails."""
        mock_openai.ChatCompletion.create.side_effect = Exception("API Error")

        result = interpreter.ai_interpret("some command")
        assert 'AI interpretation error' in result['intent']
        assert result['method'] == 'ai_error'
        assert result['confidence'] == 0.0


class TestAIInterpreterFallback:
    """Test cases for fallback interpretation."""

    def test_fallback_help(self, interpreter):
        """Test fallback for 'help' command."""
        result = interpreter.fallback_interpret("help me")
        assert result['intent'] == 'Show help information'
        assert result['method'] == 'fallback'

    def test_fallback_direct_command(self, interpreter):
        """Test fallback for what looks like a direct shell command."""
        result = interpreter.fallback_interpret("ls -l /home")
        assert result['intent'] == 'Execute shell command directly'
        assert result['commands'][0]['command'] == 'ls -l /home'
        assert 'warnings' in result

    def test_fallback_unrecognized(self, interpreter):
        """Test fallback for an unrecognized command."""
        result = interpreter.fallback_interpret("what is the time")
        assert result['intent'] == 'Command not recognized'
        assert result['commands'][0]['type'] == 'suggestion'
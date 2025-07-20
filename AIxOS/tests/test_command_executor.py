import pytest
import subprocess
from unittest.mock import MagicMock, patch
from aixos.core.config import AppConfig
from aixos.core.command_executor import CommandExecutor

@pytest.fixture
def config():
    """Fixture for AppConfig."""
    return AppConfig(command_timeout=5, max_output_lines=10)

@pytest.fixture
def executor(config):
    """Fixture for CommandExecutor."""
    return CommandExecutor(config)

class TestCommandExecutor:
    """Test cases for the CommandExecutor class."""

    def test_execute_simple_command(self, executor):
        """Test executing a simple, safe command."""
        commands = [{'command': 'echo "Hello, AIxOS!"'}]
        results = executor.execute(commands)
        
        assert len(results) == 1
        result = results[0]
        assert result['return_code'] == 0
        assert 'Hello, AIxOS!' in result['output']
        assert result['status'] == 'success'

    def test_execute_multiple_commands(self, executor):
        """Test executing a list of multiple commands."""
        commands = [
            {'command': 'echo "Command 1"'},
            {'command': 'echo "Command 2"'}
        ]
        results = executor.execute(commands)
        
        assert len(results) == 2
        assert 'Command 1' in results[0]['output']
        assert 'Command 2' in results[1]['output']

    def test_command_failure(self, executor):
        """Test a command that fails (non-zero exit code)."""
        commands = [{'command': 'ls /nonexistent-directory'}]
        results = executor.execute(commands)
        
        assert len(results) == 1
        result = results[0]
        assert result['return_code'] != 0
        assert result['status'] == 'failed'
        assert 'error' in result

    def test_dangerous_command_blocking(self, executor):
        """Test that dangerous commands are blocked."""
        dangerous_commands = [
            {'command': 'rm -rf /'},
            {'command': 'sudo rm -rf /'},
            {'command': 'shutdown -h now'}
        ]
        results = executor.execute(dangerous_commands)
        
        assert len(results) == 3
        for result in results:
            assert result['status'] == 'blocked'
            assert 'Dangerous command blocked' in result['error']

    def test_allowed_sudo_command(self, executor):
        """Test that safe sudo commands are allowed (mocked)."""
        # We can't actually run sudo, so we mock the subprocess call
        with patch('subprocess.run') as mock_run:
            mock_process = MagicMock()
            mock_process.returncode = 0
            mock_process.stdout = b'Success'
            mock_process.stderr = b''
            mock_run.return_value = mock_process

            commands = [{'command': 'sudo apt-get update'}]
            results = executor.execute(commands)
            
            assert len(results) == 1
            assert results[0]['status'] == 'success'
            mock_run.assert_called_once()

    def test_command_timeout(self, config):
        """Test that a command times out correctly."""
        # Use a shorter timeout for this test
        config.command_timeout = 1
        executor = CommandExecutor(config)
        
        # This command should take longer than 1 second
        commands = [{'command': 'sleep 2'}]
        results = executor.execute(commands)
        
        assert len(results) == 1
        result = results[0]
        assert result['status'] == 'timeout'
        assert 'Command timed out' in result['error']

    def test_max_output_lines_truncation(self, config):
        """Test that output is truncated to max_output_lines."""
        config.max_output_lines = 3
        executor = CommandExecutor(config)
        
        # This command produces more than 3 lines of output
        long_output_command = 'for i in {1..5}; do echo "Line $i"; done'
        commands = [{'command': long_output_command}]
        results = executor.execute(commands)
        
        assert len(results) == 1
        result = results[0]
        output_lines = result['output'].strip().split('\n')
        assert len(output_lines) <= config.max_output_lines + 1 # +1 for truncation message
        assert '... (output truncated)' in result['output']
import pytest
import os
import tempfile
import json
from pathlib import Path
from aixos.core.config import AppConfig


class TestAppConfig:
    """Test cases for AppConfig class."""
    
    def test_default_config(self):
        """Test default configuration values."""
        config = AppConfig()
        
        assert config.ai_model_name == "gpt-3.5-turbo"
        assert config.max_tokens == 1000
        assert config.temperature == 0.7
        assert config.vector_store_path == "./data/vector_store"
        assert config.log_level == "INFO"
        assert config.history_size == 100
        assert config.safe_mode is True
        assert config.command_timeout == 30
        assert config.max_output_lines == 50
    
    def test_config_with_custom_values(self):
        """Test configuration with custom values."""
        config = AppConfig(
            ai_model_name="gpt-4",
            max_tokens=2000,
            temperature=0.5,
            safe_mode=False
        )
        
        assert config.ai_model_name == "gpt-4"
        assert config.max_tokens == 2000
        assert config.temperature == 0.5
        assert config.safe_mode is False
    
    def test_load_from_env(self):
        """Test loading configuration from environment variables."""
        # Set environment variables
        env_vars = {
            "AI_MODEL_NAME": "llama2",
            "MODEL_PATH": "/path/to/local/model",
            "MAX_TOKENS": "1500", 
            "TEMPERATURE": "0.8",
            "SAFE_MODE": "false",
            "LOG_LEVEL": "DEBUG",
            "COMMAND_TIMEOUT": "60",
            "API_BASE": "http://localhost:1234/v1"
        }
        
        # Temporarily set environment variables
        original_env = {}
        for key, value in env_vars.items():
            original_env[key] = os.environ.get(key)
            os.environ[key] = value
        
        try:
            config = AppConfig.load_from_env()
            
            assert config.ai_model_name == "llama2"
            assert config.model_path == "/path/to/local/model"
            assert config.max_tokens == 1500
            assert config.temperature == 0.8
            assert config.safe_mode is False
            assert config.log_level == "DEBUG"
            assert config.command_timeout == 60
            assert config.ai_model_api_base == "http://localhost:1234/v1"
        finally:
            # Restore original environment
            for key, value in original_env.items():
                if value is None:
                    os.environ.pop(key, None)
                else:
                    os.environ[key] = value
    
    def test_save_and_load_config_file(self):
        """Test saving and loading configuration to/from file."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "test_config.json"
            
            # Create a config with custom values
            original_config = AppConfig(
                ai_model_name="gpt-4",
                max_tokens=2000,
                temperature=0.5,
                safe_mode=False,
                log_level="DEBUG"
            )
            
            # Save config
            original_config.save_to_file(str(config_path))
            
            # Verify file exists and has content
            assert config_path.exists()
            
            # Load config from file
            loaded_config = AppConfig.load_from_file(str(config_path))
            
            # Verify loaded config matches original
            assert loaded_config.ai_model_name == original_config.ai_model_name
            assert loaded_config.max_tokens == original_config.max_tokens
            assert loaded_config.temperature == original_config.temperature
            assert loaded_config.safe_mode == original_config.safe_mode
            assert loaded_config.log_level == original_config.log_level
    
    def test_load_from_nonexistent_file(self):
        """Test loading from a non-existent file returns default config."""
        config = AppConfig.load_from_file("/nonexistent/path/config.json")
        
        # Should return default config
        default_config = AppConfig()
        assert config.ai_model_name == default_config.ai_model_name
        assert config.max_tokens == default_config.max_tokens
    
    def test_config_validation(self):
        """Test configuration validation."""
        # Test invalid temperature (should be between 0 and 2)
        with pytest.raises(ValueError):
            AppConfig(temperature=-0.1)
        
        with pytest.raises(ValueError):
            AppConfig(temperature=2.1)
        
        # Test invalid max_tokens (should be positive)
        with pytest.raises(ValueError):
            AppConfig(max_tokens=0)
        
        with pytest.raises(ValueError):
            AppConfig(max_tokens=-100)
        
        # Test invalid command_timeout (should be positive)
        with pytest.raises(ValueError):
            AppConfig(command_timeout=0)
        
        # Test invalid history_size (should be positive)
        with pytest.raises(ValueError):
            AppConfig(history_size=0)
    
    def test_config_serialization(self):
        """Test that config can be properly serialized to JSON."""
        config = AppConfig(
            ai_model_name="gpt-4",
            max_tokens=1500,
            temperature=0.8,
            safe_mode=False
        )
        
        # Convert to dict and serialize
        config_dict = config.model_dump()
        json_str = json.dumps(config_dict)
        
        # Should not raise any exceptions
        assert isinstance(json_str, str)
        assert len(json_str) > 0
        
        # Deserialize and verify
        loaded_dict = json.loads(json_str)
        loaded_config = AppConfig(**loaded_dict)
        
        assert loaded_config.ai_model_name == config.ai_model_name
        assert loaded_config.max_tokens == config.max_tokens
        assert loaded_config.temperature == config.temperature
        assert loaded_config.safe_mode == config.safe_mode
    
    def test_env_boolean_parsing(self):
        """Test that boolean environment variables are parsed correctly."""
        test_cases = [
            ("true", True),
            ("True", True),
            ("TRUE", True),
            ("1", True),
            ("yes", True),
            ("false", False),
            ("False", False),
            ("FALSE", False),
            ("0", False),
            ("no", False),
            ("", False),
        ]
        
        for env_value, expected in test_cases:
            os.environ["SAFE_MODE"] = env_value
            try:
                config = AppConfig.load_from_env()
                assert config.safe_mode == expected, f"Failed for env_value: {env_value}"
            finally:
                os.environ.pop("SAFE_MODE", None)
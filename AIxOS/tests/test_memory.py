import pytest
import tempfile
import os
from pathlib import Path
from unittest.mock import MagicMock, patch
from aixos.core.config import AppConfig
from aixos.core.memory import MemoryManager

@pytest.fixture
def config():
    """Fixture for AppConfig with a temporary vector store path."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield AppConfig(vector_store_path=str(Path(temp_dir) / "test_db"))

@pytest.fixture
def memory_manager(config):
    """Fixture for MemoryManager."""
    # Mock ChromaDB client to avoid actual DB operations in most tests
    with patch('aixos.core.memory.chromadb.PersistentClient') as mock_client:
        manager = MemoryManager(config)
        manager.db_client = mock_client.return_value
        manager.interactions_collection = MagicMock()
        manager.patterns_collection = MagicMock()
        yield manager

class TestMemoryManager:
    """Test cases for the MemoryManager class."""

    def test_initialization(self, config):
        """Test that MemoryManager initializes correctly and creates directories."""
        assert Path(config.vector_store_path).exists()
        assert Path(config.vector_store_path).is_dir()

    def test_store_interaction(self, memory_manager):
        """Test storing a single interaction."""
        interaction = {
            'user_input': 'list files',
            'interpretation': {'commands': [{'command': 'ls -la'}]},
            'execution_results': [{'status': 'success'}]
        }
        memory_manager.store_interaction(interaction)

        memory_manager.interactions_collection.add.assert_called_once()
        call_args = memory_manager.interactions_collection.add.call_args[1]
        assert 'list files' in call_args['documents'][0]
        assert 'ls -la' in call_args['documents'][0]
        assert 'interaction_id' in call_args['metadatas'][0]

    def test_update_successful_pattern(self, memory_manager):
        """Test updating successful command patterns."""
        interaction = {
            'user_input': 'show directory contents',
            'interpretation': {
                'intent': 'list files',
                'commands': [{'command': 'ls -la', 'description': 'list files'}]
            },
            'execution_results': [{'status': 'success', 'return_code': 0}]
        }
        memory_manager.update_successful_patterns(interaction)

        memory_manager.patterns_collection.add.assert_called_once()
        call_args = memory_manager.patterns_collection.add.call_args[1]
        assert call_args['documents'][0] == 'list files'
        assert call_args['metadatas'][0]['command'] == 'ls -la'

    def test_retrieve_similar_interactions(self, memory_manager):
        """Test retrieving similar interactions."""
        mock_retrieval_result = {
            'ids': [['id1']],
            'documents': [['doc1']],
            'metadatas': [[{'user_input': 'show files'}]]
        }
        memory_manager.interactions_collection.query.return_value = mock_retrieval_result

        results = memory_manager.retrieve_similar_interactions("list all files")
        
        memory_manager.interactions_collection.query.assert_called_with(
            query_texts=["list all files"],
            n_results=5
        )
        assert len(results) == 1
        assert results[0]['user_input'] == 'show files'

    def test_retrieve_successful_patterns(self, memory_manager):
        """Test retrieving successful patterns based on intent."""
        mock_retrieval_result = {
            'ids': [['id1']],
            'documents': [['list files']],
            'metadatas': [[{'command': 'ls -la', 'description': 'list files'}]]
        }
        memory_manager.patterns_collection.query.return_value = mock_retrieval_result

        results = memory_manager.retrieve_successful_patterns("list files")

        memory_manager.patterns_collection.query.assert_called_with(
            query_texts=["list files"],
            n_results=3
        )
        assert len(results) == 1
        assert results[0]['command'] == 'ls -la'

    def test_no_pattern_update_on_failure(self, memory_manager):
        """Test that patterns are not updated if command execution fails."""
        interaction = {
            'user_input': 'delete everything',
            'interpretation': {'commands': [{'command': 'rm -rf /'}]},
            'execution_results': [{'status': 'failed'}]
        }
        memory_manager.update_successful_patterns(interaction)

        memory_manager.patterns_collection.add.assert_not_called()

# Integration-style test to check real DB interaction
@pytest.mark.integration
def test_memory_manager_integration(config):
    """Test MemoryManager with a real ChromaDB instance."""
    # This test will create a real DB in the temp directory
    manager = MemoryManager(config)

    # Store an interaction
    interaction = {
        'user_input': 'create a test file',
        'interpretation': {
            'intent': 'create file',
            'commands': [{'command': 'touch test.txt', 'description': 'create file'}]
        },
        'execution_results': [{'status': 'success', 'return_code': 0}]
    }
    manager.store_interaction(interaction)
    manager.update_successful_patterns(interaction)

    # Retrieve similar interactions
    similar = manager.retrieve_similar_interactions('make a file')
    assert len(similar) > 0
    assert 'create a test file' in similar[0]['document']

    # Retrieve successful patterns
    patterns = manager.retrieve_successful_patterns('create file')
    assert len(patterns) > 0
    assert patterns[0]['command'] == 'touch test.txt'
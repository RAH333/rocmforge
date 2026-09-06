import os
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
from src.main import ROCmForgeEngine
from src.tools.code_parser import read_target_file

# Setup fixture to initialize the engine before each test run
@pytest.fixture
def test_engine(monkeypatch):
    # Mock environment variables to prevent actual network calls during testing
    monkeypatch.setenv("AMD_CLOUD_API_BASE", "https://api.com")
    monkeypatch.setenv("AMD_CLOUD_API_KEY", "mock-token-12345")
    return ROCmForgeEngine()

def test_config_files_loading(test_engine):
    """Verify that YAML configuration patterns load properly and are not empty."""
    assert test_engine.agents_config is not None
    assert test_engine.tasks_config is not None
    
    # Assert structural integrity of configurations
    assert "code_porting_agent" in test_engine.agents_config
    assert "port_codebase_task" in test_engine.tasks_config

def test_code_parser_tool_missing_file():
    """Verify the file reading tool handles missing target paths gracefully."""
    bad_path = "non_existent_file_path_xyz.py"
    response = read_target_file(bad_path)
    assert "Error:" in response
    assert bad_path in response

def test_code_parser_tool_valid_file(tmp_path):
    """Verify the file reading tool correctly returns local file string blocks."""
    # Create an isolated temporary file using pytest utilities
    temp_file = tmp_path / "mock_code.py"
    mock_content = "import torch\nprint('hello from CUDA')"
    temp_file.write_text(mock_content, encoding='utf-8')
    
    response = read_target_file(str(temp_file))
    assert response == mock_content

@patch('src.main.Crew')
def test_pipeline_orchestration_trigger(mock_crew_class, test_engine, tmp_path):
    """Verify the sequential agent flow initializes and starts with correct parameters."""
    # Setup temporary file execution anchor
    temp_file = tmp_path / "target_test.py"
    temp_file.write_text("import pycuda", encoding='utf-8')
    
    # Setup mock instances to isolate local system dependencies
    mock_crew_instance = MagicMock()
    mock_crew_instance.kickoff.return_value = "Mocked optimization analysis report completed."
    mock_crew_class.return_value = mock_crew_instance
    
    result = test_engine.initialize_orchestration(str(temp_file))
    
    # Validate orchestration triggers correctly
    mock_crew_class.assert_called_once()
    mock_crew_instance.kickoff.assert_called_once_with(inputs={"file_path": str(temp_file)})
    assert "Mocked" in result
  

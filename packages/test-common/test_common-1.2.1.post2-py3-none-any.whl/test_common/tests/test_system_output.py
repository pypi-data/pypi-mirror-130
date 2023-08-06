"""
Tests for system.output module.
"""
import pytest
import test_common.system.output as system_output


@pytest.mark.output
def test_log_function_output():
    with system_output.OutputLogger.get_logger() as logger:
        expected_value = "Hello world!"
        print(expected_value)
        assert logger.output.rstrip("\n") == expected_value

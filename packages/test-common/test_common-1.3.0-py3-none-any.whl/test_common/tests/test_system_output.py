"""
Tests for system.output module.
"""
import pytest
import test_common.system.output as system_output


@pytest.mark.output
def test_log_function_output():
    with system_output.OutputLogger.get_logger() as logger:
        expected_value = "Hello world!"
        expected_value_2 = "Bye"
        print(expected_value)
        assert expected_value in logger.output
        print(expected_value_2)
        assert logger.output[1] == expected_value_2

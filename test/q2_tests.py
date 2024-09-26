import pytest
from datetime import date
from ..src.q2_memory import q2_memory
from ..src.q2_time import q2_time

file_path = "test/resources/twitter_test.json"


def test_q2():

    q2_memory_result = q2_memory(file_path)
    q2_time_result = q2_time(file_path)

    expected_results = [('🤫', 2), ('🤔', 2), ('🌾', 1), ('🚜', 1), ('💪', 1)]

    assert q2_memory_result == expected_results
    assert q2_time_result == expected_results

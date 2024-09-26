import pytest
from datetime import date
from ..src.q1_memory import q1_memory
from ..src.q1_time import q1_time

file_path = "test/resources/twitter_test.json"


def test_q1():

    q1_memory_result = q1_memory(file_path)
    q1_time_result = q1_time(file_path)

    expected_results = [(date(2021, 2, 24), 'anmoldhaliwal')]

    assert q1_memory_result == expected_results
    assert q1_time_result == expected_results

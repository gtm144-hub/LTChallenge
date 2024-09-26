import pytest
from datetime import date
from ..src.q3_memory import q3_memory
from ..src.q3_time import q3_time

file_path = "test/resources/twitter_test.json"


def test_q3():

    q3_memory_result = q3_memory(file_path)
    q3_time_result = q3_time(file_path)

    expected_results = [('mandeeppunia1', 2),
                         ('DelhiPolice', 1),
                         ('Kisanektamorcha', 1),
                         ('ReallySwara', 1),
                         ('narendramodi', 1),
                         ('rohini_sgh', 1)]

    assert q3_memory_result == expected_results
    assert q3_time_result == expected_results

# content of conftest.py
import pytest
from pygems.core.timer import Timer
from functools import partial



@pytest.fixture(autouse=True)
def add_np(doctest_namespace):
    doctest_namespace["time_func"] = partial([1, 9.1234, 30.789].pop, 0)
    doctest_namespace["stop_func"] = lambda t, *args: print(f'{t.name}:', *args, f'{round(t.elapsed,6)}s')

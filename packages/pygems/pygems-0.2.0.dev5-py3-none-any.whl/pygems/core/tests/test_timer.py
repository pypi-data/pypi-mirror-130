from unittest import mock
from pygems.core import timer

class TestTimer:
    def test_time_attribute_returns_timer_func(self):
        time_func = mock.Mock
        t = timer.Timer(time_func=time_func)
        assert time_func is t.time_func

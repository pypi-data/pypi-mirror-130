import pytest
from unittest import mock
from pygems.core import shortcuts

class TestDropFields:
    def test_returns_argument(self):
        data = { 'name': 'John', 'age': 32 }
        result = shortcuts.drop_fields(data, 'age')
        assert result is data

    def test_drops_single_field(self):
        data = { 'name': 'John', 'age': 32 }
        result = shortcuts.drop_fields(data, 'age')
        assert result == { 'name': 'John' }
    
    def test_drops_multiple_field(self):
        data = { 'name': 'John', 'age': 32, 'sex': 'shemale' }
        result = shortcuts.drop_fields(data, ('age', 'sex'))
        assert result == { 'name': 'John' }

    def test_raises_key_error_missing_field(self):
        data = { 'name': 'John' }
        with pytest.raises(KeyError):
            shortcuts.drop_fields(data, 'age')

    def test_calls_error_handler(self):
        data = { 'name': 'John' }
        fake_handler = mock.Mock()
        shortcuts.drop_fields(data, 'age', fake_handler)
        fake_handler.assert_called_once()

class TestGetIgnoreErrors:
    def test_returns_callable(self):
        handler = shortcuts.get_ignore_errors(KeyError)
        assert callable(handler)

    def test_handler_raises_unspecified_errors(self):
        handler = shortcuts.get_ignore_errors(ArithmeticError)
        with pytest.raises(KeyError):
            handler(KeyError())


class TestGetattrNested:

    def test_returns_nested_attribute(self):
        user = mock.MagicMock()
        user.address.city = 'Sofia'
        actual = shortcuts.getattr_nested(user, 'address.city')
        assert 'Sofia' == actual

    def test_returns_default_value_when_specified_and_attribute_is_missing(self):
        user = 'john'
        actual = shortcuts.getattr_nested(user, 'address.city', 'Mexico')
        assert 'Mexico' == actual

    def test_raises_attribute_error_when_attribute_is_missing(self):
        user = 'john'
        with pytest.raises(AttributeError):
            shortcuts.getattr_nested(user, 'address.city')


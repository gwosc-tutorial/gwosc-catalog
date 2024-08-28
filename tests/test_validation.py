from ccverify import validate_schema
import pytest


def test_global_keys():
    bad_keys = {"a": 1, "b": 2}
    with pytest.raises((KeyError, ValueError)):
        validate_schema(bad_keys)

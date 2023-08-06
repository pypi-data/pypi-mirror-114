from jsonschema import Draft7Validator

from namefiles import register_filename_validator
import pytest


def test_register_exceptions():
    sample_naming_convention = {}
    with pytest.raises(AttributeError):
        register_filename_validator({})

    with pytest.raises(KeyError):
        from jsonschema import Draft7Validator
        register_filename_validator(Draft7Validator({}))

    test_convention = {
        "name": "test_convention",
    }
    assert register_filename_validator(Draft7Validator(test_convention))


def test_register_already_registered():
    test_convention = {
        "name": "2nd_test_convention",
    }
    assert register_filename_validator(Draft7Validator(test_convention))
    assert not register_filename_validator(Draft7Validator(test_convention))

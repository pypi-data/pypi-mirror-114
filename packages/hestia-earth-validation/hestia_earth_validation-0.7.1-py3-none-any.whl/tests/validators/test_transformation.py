import json

from tests.utils import fixtures_path
from hestia_earth.validation.validators.transformation import (
    validate_previous_transformation,
    validate_first_transformation
)

fixtures_folder = f"{fixtures_path}/transformation"


def test_validate_previous_transformation_valid():
    # no transformations should be valid
    assert validate_previous_transformation([])

    with open(f"{fixtures_folder}/previousTransformationTerm/valid.json") as f:
        data = json.load(f)
    assert validate_previous_transformation(data.get('nodes')) is True


def test_validate_previous_transformation_invalid():
    with open(f"{fixtures_folder}/previousTransformationTerm/invalid-wrong-order.json") as f:
        data = json.load(f)
    assert validate_previous_transformation(data.get('nodes')) == {
        'level': 'error',
        'dataPath': '.transformations[1].previousTransformationTerm',
        'message': 'must point to a previous transformation in the list'
    }

    with open(f"{fixtures_folder}/previousTransformationTerm/invalid-no-previous.json") as f:
        data = json.load(f)
    assert validate_previous_transformation(data.get('nodes')) == {
        'level': 'error',
        'dataPath': '.transformations[1].previousTransformationTerm',
        'message': 'must point to a previous transformation in the list'
    }

    with open(f"{fixtures_folder}/previousTransformationTerm/invalid-product-input.json") as f:
        data = json.load(f)
    assert validate_previous_transformation(data.get('nodes')) == {
        'level': 'error',
        'dataPath': '.transformations[1].inputs[0].value',
        'message': 'must be equal to previous product multiplied by the share'
    }


def test_validate_first_transformation_valid():
    # no transformations should be valid
    assert validate_first_transformation([])

    with open(f"{fixtures_folder}/first-transformation/valid.json") as f:
        data = json.load(f)
    assert validate_first_transformation(data.get('nodes')) is True


def test_validate_first_transformation_invalid():
    with open(f"{fixtures_folder}/first-transformation/invalid.json") as f:
        data = json.load(f)
    assert validate_first_transformation(data.get('nodes')) == {
        'level': 'error',
        'dataPath': '.transformations[0].previousTransformationTerm',
        'message': 'must not be set on the first transformation'
    }

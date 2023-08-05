from hestia_earth.schema import SchemaType, TermTermType
from hestia_earth.utils.api import find_node
from hestia_earth.utils.lookup import download_lookup, get_table_value, column_name

from hestia_earth.validation.utils import _filter_list_errors


def _methodModels():
    terms = find_node(SchemaType.TERM, {'termType': TermTermType.MODEL.value}, limit=1000)
    return [term.get('@id') for term in terms if term.get('@id')]


def _allowed_characterisedIndicator_model(lookup, models: list, term_id: str):
    return [m for m in models if m != 'termid' and get_table_value(lookup, 'termid', term_id, column_name(m))]


def _is_method_allowed(lookup, term_id: str, model: str):
    value = get_table_value(lookup, 'termid', term_id, column_name(model))
    # bug numpy bool not returning `True`
    return True if value else False


def validate_characterisedIndicator_model(node: dict, list_key: str):
    lookup = download_lookup('characterisedIndicator-model-mapping.csv')
    models = _methodModels()

    def validate(values: tuple):
        index, value = values
        term_id = value.get('term', {}).get('@id')
        model = value.get('methodModel', {}).get('@id')
        should_validate = term_id in list(lookup.termid) and model is not None
        return not should_validate or _is_method_allowed(lookup, term_id, model) or {
            'level': 'error',
            'dataPath': f".{list_key}[{index}].methodModel.@id",
            'message': 'is not allowed for this characterisedIndicator',
            'params': {
                'allowedValues': _allowed_characterisedIndicator_model(lookup, models, term_id)
            }
        }

    return _filter_list_errors(list(map(validate, enumerate(node.get(list_key, [])))))

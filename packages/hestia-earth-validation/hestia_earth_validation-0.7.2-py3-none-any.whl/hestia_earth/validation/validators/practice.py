from hestia_earth.schema import TermTermType
from hestia_earth.utils.model import find_term_match
from hestia_earth.utils.tools import flatten, list_sum

from hestia_earth.validation.utils import _filter_list


def validate_longFallowPeriod(practices: list):
    longFallowPeriod = find_term_match(practices, 'longFallowPeriod', None)
    longFallowPeriod_index = practices.index(longFallowPeriod) if longFallowPeriod else 0
    value = list_sum(longFallowPeriod.get('value', [0])) if longFallowPeriod else 0
    rotationDuration = list_sum(find_term_match(practices, 'rotationDuration').get('value', 0))
    return value == 0 or ((rotationDuration - value) / value) < 5 or {
        'level': 'error',
        'dataPath': f".practices[{longFallowPeriod_index}].value",
        'message': 'longFallowPeriod must be lower than 5 years'
    }


def validate_cropResidueManagement(practices: list):
    practices = _filter_list(practices, 'term.termType', TermTermType.CROPRESIDUEMANAGEMENT.value)
    sum = list_sum(flatten([p.get('value', []) for p in practices]))
    return sum <= 100.5 or {
        'level': 'error',
        'dataPath': '.practices',
        'message': 'value should sum to 100 or less across crop residue management practices',
        'params': {
            'sum': sum
        }
    }

from functools import reduce
from hestia_earth.validation.validators.shared import value_difference
from hestia_earth.utils.model import find_term_match
from hestia_earth.utils.lookup import download_lookup, get_table_value, column_name
from hestia_earth.utils.tools import list_sum, non_empty_list, safe_parse_float, flatten

from hestia_earth.validation.utils import _filter_list_errors, _value_range_error, _value_average, _node_year
from hestia_earth.validation.gee import fetch_data
from .shared import need_validate_coordinates


SOIL_TEXTURE_IDS = ['sandContent', 'siltContent', 'clayContent']


def _rainfallAnnual(site: dict, measurement: dict):
    year = _node_year(measurement)
    value = fetch_data(collection='ECMWF/ERA5/MONTHLY',
                       ee_type='raster_by_period',
                       band_name='total_precipitation',
                       reducer='sum',
                       reducer_regions='mean',
                       year=str(year),
                       latitude=site.get('latitude'),
                       longitude=site.get('longitude')
                       ).get('mean', None) if need_validate_coordinates(site) and year else None
    return value * 1000 if value else None


MEASUREMENTS_MODELS = {
    'rainfallAnnual': _rainfallAnnual
}


def _group_measurement_key(measurement: dict):
    keys = non_empty_list([
        str(measurement.get('depthUpper', '')),
        str(measurement.get('depthLower', '')),
        measurement.get('startDate'),
        measurement.get('endDate')
    ])
    return '-'.join(keys) if len(keys) > 0 else 'default'


def _group_measurements_depth(measurements: list):
    def group_by(group: dict, measurement: dict):
        key = _group_measurement_key(measurement)
        if key not in group:
            group[key] = []
        group[key].extend([measurement])
        return group

    return reduce(group_by, measurements, {})


def _validate_soilTexture_percent(lookup):
    soil_texture_ids = list(lookup.termid)

    def validate_single(measurements: list, measurement: dict, texture_id: str):
        texture = find_term_match(measurements, texture_id, {})
        term_id = measurement['term']['@id']
        min = safe_parse_float(get_table_value(lookup, 'termid', term_id, column_name(f"{texture_id}min")), 0)
        max = safe_parse_float(get_table_value(lookup, 'termid', term_id, column_name(f"{texture_id}max")), 100)
        # set default value to min so if no value then passes validation
        texture_value = _value_average(texture, min)
        return min <= texture_value <= max or {
            'level': 'error',
            'dataPath': '.measurements',
            'message': 'is outside the allowed range',
            'params': {
                'term': texture['term'],
                'range': {'min': min, 'max': max}
            }
        }

    def validate_all(measurements: list):
        values = list(filter(lambda v: v['term']['@id'] in soil_texture_ids, measurements))
        return len(values) == 0 or flatten(map(
            lambda measurement: list(map(lambda id: validate_single(measurements, measurement, id), SOIL_TEXTURE_IDS)),
            values
        ))

    return validate_all


def _validate_soiltTexture_sum(measurements: list):
    measurements = list(filter(lambda v: v['term']['@id'] in SOIL_TEXTURE_IDS, measurements))
    measurements = list(filter(lambda v: 'value' in v, measurements))
    terms = list(map(lambda v: v['term']['@id'], measurements))
    sum_values = sum(map(lambda v: _value_average(v), measurements))
    return len(set(terms)) != len(SOIL_TEXTURE_IDS) or 99.5 < sum_values < 100.5 or {
        'level': 'error',
        'dataPath': '.measurements',
        'message': f"sum not equal to 100% for {', '.join(SOIL_TEXTURE_IDS)}"
    }


def validate_soilTexture(measurements: list):
    soilTexture = download_lookup('soilTexture.csv', True)
    groupped_measurements = _group_measurements_depth(measurements).values()
    results_sum = list(map(_validate_soiltTexture_sum, groupped_measurements))
    valid_sum = next((x for x in results_sum if x is not True), True)
    results_percent = flatten(map(_validate_soilTexture_percent(soilTexture), groupped_measurements))
    valid_percent = next((x for x in results_percent if x is not True), True)
    return valid_sum if valid_sum is not True else valid_percent


def validate_depths(measurements: list):
    def validate(values: tuple):
        index, measurement = values
        return measurement.get('depthUpper', 0) < measurement.get('depthLower', 1) or {
            'level': 'error',
            'dataPath': f".measurements[{index}].depthLower",
            'message': 'must be greater than depthUpper'
        }

    return _filter_list_errors(map(validate, enumerate(measurements)))


def validate_value_min_max(measurements: list):
    lookup = download_lookup('measurement.csv', True)

    def validate(values: tuple):
        index, measurement = values
        term_id = measurement.get('term', {}).get('@id')
        mininum = safe_parse_float(get_table_value(lookup, 'termid', term_id, 'minimum'), None)
        maximum = safe_parse_float(get_table_value(lookup, 'termid', term_id, 'maximum'), None)
        value = _value_average(measurement)
        error = _value_range_error(value, mininum, maximum) if value is not None else False
        return error is False or ({
            'level': 'error',
            'dataPath': f".measurements[{index}].value",
            'message': f"should be above {mininum}"
        } if error == 'minimum' else {
            'level': 'error',
            'dataPath': f".measurements[{index}].value",
            'message': f"should be below {maximum}"
        })

    return _filter_list_errors(map(validate, enumerate(measurements)))


def validate_term_unique(measurements: list):
    lookup = download_lookup('measurement.csv', True)

    def count_same_term(term_id: str):
        return len(list(filter(lambda x: x.get('term', {}).get('@id') == term_id, measurements)))

    def validate(values: tuple):
        index, measurement = values
        term_id = measurement.get('term', {}).get('@id')
        unique = get_table_value(lookup, 'termid', term_id, 'onemeasurementpersite')
        unique = False if unique is None or unique == '-' else bool(unique)
        return not unique or count_same_term(term_id) == 1 or {
            'level': 'error',
            'dataPath': f".measurements[{index}].term.name",
            'message': 'must be unique'
        }

    return _filter_list_errors(map(validate, enumerate(measurements)))


def validate_require_startDate_endDate(measurements: list):
    lookup = download_lookup('measurement.csv', True)

    def validate(values: tuple):
        index, measurement = values
        term_id = measurement.get('term', {}).get('@id')
        start_date = measurement.get('startDate')
        end_date = measurement.get('endDate')
        required = get_table_value(lookup, 'termid', term_id, column_name('needStartDateEndDate'))
        return not required or (start_date is not None and end_date is not None) or [
            {
                'level': 'error',
                'dataPath': f".measurements[{index}].startDate",
                'message': 'is required'
            },
            {
                'level': 'error',
                'dataPath': f".measurements[{index}].endDate",
                'message': 'is required'
            }
        ]

    return _filter_list_errors(flatten(map(validate, enumerate(measurements))))


def validate_with_models(site: dict, list_key: str):
    def validate(values: tuple):
        index, blank_node = values
        term_id = blank_node.get('term', {}).get('@id')
        value = blank_node.get('value', [0])
        value = list_sum(value, value)
        expected_value = MEASUREMENTS_MODELS[term_id](site, blank_node) if term_id in MEASUREMENTS_MODELS else value
        delta = value_difference(value, expected_value) if expected_value else 0
        return delta < 0.25 or {
            'level': 'warning',
            'dataPath': f".{list_key}[{index}].value",
            'message': 'the measurement provided might be in error',
            'params': {
                'term': blank_node.get('term', {}),
                'current': value,
                'expected': expected_value,
                'delta': delta * 100
            }
        }

    return _filter_list_errors(flatten(map(validate, enumerate(site.get(list_key, [])))))

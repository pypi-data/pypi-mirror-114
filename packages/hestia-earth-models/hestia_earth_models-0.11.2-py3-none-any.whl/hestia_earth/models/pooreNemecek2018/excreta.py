from hestia_earth.schema import ProductStatsDefinition
from hestia_earth.utils.model import find_primary_product, find_term_match
from hestia_earth.utils.lookup import get_table_value, download_lookup

from hestia_earth.models.log import debugRequirements, logger
from hestia_earth.models.utils.product import _new_product, animal_produced
from hestia_earth.models.utils.input import get_feed_nitrogen
from hestia_earth.models.utils.term import get_excreta_terms
from . import MODEL


def _product(value: float, excreta: str):
    logger.info('model=%s, term=%s, value=%s', MODEL, excreta, value)
    product = _new_product(excreta, MODEL)
    product['value'] = [value]
    product['statsDefinition'] = ProductStatsDefinition.MODELLED.value
    return product


def _no_excreta_term(products: list):
    term_ids = get_excreta_terms()
    return all([not find_term_match(products, term) for term in term_ids])


def _get_excreta_term(cycle: dict):
    primary_prod = find_primary_product(cycle) or {}
    term_id = primary_prod.get('term', {}).get('@id')
    term_type = primary_prod.get('term', {}).get('termType')
    lookup = download_lookup(f"{term_type}.csv", True)
    return get_table_value(lookup, 'termid', term_id, 'excreta')


def _run(inputs_n: float, products_n: float, excreta: str):
    value = (inputs_n - products_n) / 100
    return [_product(value, excreta)]


def _should_run(cycle: dict):
    excreta = _get_excreta_term(cycle)
    dc = cycle.get('dataCompleteness', {})
    is_complete = dc.get('animalFeed', False) and dc.get('products', False)
    inputs = cycle.get('inputs', [])
    inputs_n = get_feed_nitrogen(inputs)
    products = cycle.get('products', [])
    products_n = animal_produced(products)
    no_excreta = _no_excreta_term(products)

    debugRequirements(model=MODEL, term=excreta,
                      inputs_n=inputs_n,
                      products_n=products_n,
                      no_excreta=no_excreta)

    should_run = all([is_complete, inputs_n, products_n, excreta, no_excreta])
    logger.info('model=%s, term=%s, should_run=%s', MODEL, excreta, should_run)
    return should_run, inputs_n, products_n, excreta


def run(cycle: dict):
    should_run, inputs_n, products_n, excreta = _should_run(cycle)
    return _run(inputs_n, products_n, excreta) if should_run else []

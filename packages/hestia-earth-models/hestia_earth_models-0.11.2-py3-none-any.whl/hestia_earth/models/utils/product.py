from hestia_earth.schema import SchemaType, TermTermType
from hestia_earth.utils.api import download_hestia
from hestia_earth.utils.model import filter_list_term_type, find_term_match, linked_node
from hestia_earth.utils.tools import list_sum

from hestia_earth.models.utils.blank_node import get_total_value_converted
from . import _term_id, _include_methodModel, _filter_list_term_unit
from .constant import Units
from .property import _get_nitrogen_content, get_node_property


def _new_product(term, model=None):
    node = {'@type': SchemaType.PRODUCT.value}
    node['term'] = linked_node(term if isinstance(term, dict) else download_hestia(_term_id(term)))
    return _include_methodModel(node, model)


def abg_total_residue_nitrogen(products: list):
    """
    Get the total above ground nitrogen content from the `aboveGroundCropResidueTotal` product.

    Parameters
    ----------
    products : list
        List of `Product`s.

    Returns
    -------
    float
        The total value as a number.
    """
    return _get_nitrogen_content(find_term_match(products, 'aboveGroundCropResidueTotal'))


def abg_residue_nitrogen(products: list):
    """
    Get the total nitrogen content from all the `aboveGroundCropResidue` products.

    Parameters
    ----------
    products : list
        List of `Product`s.

    Returns
    -------
    float
        The total value as a number.
    """
    left_on_field = find_term_match(products, 'aboveGroundCropResidueLeftOnField').get('value', [0])
    incorporated = find_term_match(products, 'aboveGroundCropResidueIncorporated').get('value', [0])
    return list_sum(left_on_field + incorporated) * abg_total_residue_nitrogen(products) / 100


def blg_residue_nitrogen(products: list):
    """
    Get the total nitrogen content from the `belowGroundCropResidue` product.

    Parameters
    ----------
    products : list
        List of `Product`s.

    Returns
    -------
    float
        The total value as a number.
    """
    residue = find_term_match(products, 'belowGroundCropResidue')
    return list_sum(residue.get('value', [0])) * _get_nitrogen_content(residue) / 100


def residue_nitrogen(products: list) -> float:
    """
    Get the total nitrogen content from the `cropResidue` products.

    Parameters
    ----------
    products : list
        List of `Product`s.

    Returns
    -------
    float
        The total value as a number.
    """
    return abg_residue_nitrogen(products) + blg_residue_nitrogen(products)


def animal_produced(products: list, prop: str = 'nitrogenContent') -> float:
    products = (
        filter_list_term_type(products, TermTermType.LIVEANIMAL) +
        filter_list_term_type(products, TermTermType.ANIMALPRODUCT)
    )

    kg = _filter_list_term_unit(products, Units.KG)
    kg_liveweight = _filter_list_term_unit(products, Units.KG_LIVEWEIGHT)
    kg_carcass = _filter_list_term_unit(products, Units.KG_CARCASS_WEIGHT)

    def product_value(product: dict):
        property = get_node_property(product, prop)
        units = product.get('term', {}).get('units', {})
        value = list_sum(get_total_value_converted([product], 'processingConversionLiveweightToCarcassWeight', False)
                         if units == Units.KG_CARCASS_WEIGHT.value else product.get('value', []))
        return value * property.get('value') if property else 0

    return list_sum(list(map(product_value, kg + kg_liveweight + kg_carcass)))

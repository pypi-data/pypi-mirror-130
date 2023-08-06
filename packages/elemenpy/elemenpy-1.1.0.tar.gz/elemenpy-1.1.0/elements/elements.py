"""A little utility module for element properties."""

from elements.classes import elements_dict

def symbol(atomic_number: int) -> str:
    """
    Returns the element symbol of a given atomic number.
    parameters: atomic number (int)
    """
    return elements_dict[atomic_number].get_symbol()

def mass(atomic_number: int) -> float:
    """
    Returns the atomic mass of a given element.
    parameters: atomic number (int)
    """
    return elements_dict[atomic_number].get_mass()

def name(atomic_number: int) -> str:
    """
    Returns the name of a given element.
    parameters: atomic number (int)
    """
    return elements_dict[atomic_number].get_name()

def group(atomic_number: int) -> str:
    """
    Returns the group of a given element.
    parameters: atomic number (int)
    """
    return elements_dict[atomic_number].get_group()

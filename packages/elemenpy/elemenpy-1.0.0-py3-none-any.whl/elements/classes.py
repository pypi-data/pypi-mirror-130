"""Element class for elements.py"""
import lists

class Element:
    """
    Element class
    Instance variables: name, symbol, number, mass
    Methods: get_name, get_symbol, get_number, get_mass
    """
    def __init__(self, name, symbol, number, mass):
        self.name = name
        self.symbol = symbol
        self.number = number
        self.mass = mass

    def get_name(self):
        """
        Get element name
        """
        return self.name

    def get_symbol(self):
        """
        Get element symbol
        """
        return self.symbol

    def get_number(self):
        """
        Get element number
        """
        return self.number

    def get_mass(self):
        """
        Get element mass
        """
        return self.mass

elements_dict = {
    1: Element('Hydrogen', 'H', 1, 1.00794),
}

for i in range(2, 119):
    elements_dict[i] = Element(
        lists.names[i - 2],
        lists.symbols[i - 2],
        lists.numbers[i - 2],
        lists.masses[i - 2]
        )

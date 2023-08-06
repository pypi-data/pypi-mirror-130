from elements.classes import elements_dict

def test_classes_element_dict():
    """
    Test the elements dictionary.
    """
    assert elements_dict[1].get_name() == 'Hydrogen'
    assert elements_dict[1].get_number() == 1
    assert elements_dict[1].get_symbol() == 'H'
    assert elements_dict[1].get_mass() == 1.00794
    assert elements_dict[1].get_group() == '1'
    assert elements_dict[89].get_name() == 'Actinium'
    assert elements_dict[89].get_symbol() == 'Ac'
    assert elements_dict[89].get_number() == 89
    assert elements_dict[89].get_mass() == 227
    assert elements_dict[89].get_group() == 'Actinide'
    assert elements_dict[118].get_name() == 'Oganesson'
    assert elements_dict[118].get_symbol() == 'Og'
    assert elements_dict[118].get_number() == 118
    assert elements_dict[118].get_mass() == 294
    assert elements_dict[118].get_group() == '18'

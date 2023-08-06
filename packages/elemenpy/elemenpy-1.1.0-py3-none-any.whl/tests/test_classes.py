from elements.classes import Element

def test_classes():
    """
    Test Element class instantiation.
    """
    cesium = Element('Cesium', 'Cs', 55, 132.9054519, "1")

    assert cesium.get_name() == 'Cesium'
    assert cesium.get_number() == 55
    assert cesium.get_symbol() == 'Cs'
    assert cesium.get_mass() == 132.9054519
    assert cesium.get_group() == "1"

    neodymium = Element('Neodymium', 'Nd', 60, 144.24, "Lanthanide")

    assert neodymium.get_name() == 'Neodymium'
    assert neodymium.get_number() == 60
    assert neodymium.get_symbol() == 'Nd'
    assert neodymium.get_mass() == 144.24
    assert neodymium.get_group() == "Lanthanide"

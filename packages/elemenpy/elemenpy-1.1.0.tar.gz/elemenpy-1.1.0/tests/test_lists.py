from elements import lists

def test_lists():
    """
    Test certain indexes of the elements lists.
    """
    assert lists.masses[0] == 4.0026
    assert lists.names[15] == 'Chlorine'
    assert lists.symbols[27] == 'Cu'
    assert lists.numbers[0] == 2
    assert lists.groups[14] == '16'

from elements import elements

def test_elements_function_integration():
    """
    Test integration of the elements module as a whole.
    Calls elements.py, which calls elements_dict in classes.py, which is populated
    by lists.py.
    """
    assert elements.symbol(1) == 'H'
    assert elements.name(27) == 'Cobalt'
    assert elements.mass(59) == 140.9077
    assert elements.group(56) == '2'

def test_add_two():
    x = 1
    y = 2
    assert x + y == 3
    
def test_dict_contains():
    my_dict = {"pi": 3.14159, "lang": 'python 3'}
    excepted = {"pi": 3.14159}
    
    assert excepted.items() <= my_dict.items()
    
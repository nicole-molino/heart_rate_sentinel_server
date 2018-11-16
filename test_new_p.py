from builtins import ValueError

import pytest
from validate_new_patient import check_if_new

def test_check_new_p_1():
    all_id= [1, 2, 3, 4, 5, 6]
    my_id= 2

    with pytest.raises(ValueError):
        check_if_new(all_id,my_id)


def test_check_new_p_2():
    all_id= [1, 2, 3, 4, 5, 6]
    my_id= 16

    a = check_if_new(all_id, my_id)

    assert a == 1
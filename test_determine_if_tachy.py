import pytest
from determine_if_tachy import determine_if_tachy


def test_tachy_under_age():
    age = .01
    HR = 100
    with pytest.raises(ValueError):
        determine_if_tachy(age, HR)


@pytest.mark.parametrize("age,HR,expected", [
    (3.5, 170, 1),
    (20, 150, 1),
    (20, 90, 0),
    (9, 130, 0),
    (10, 150, 1),
    (.5, 50, 0),
    ((7 / 12), 170, 1),
    ((7 / 12), 1, 0)
])
def test_tachy_parametrize(age, HR, expected):
    """test_tachy_paramaterize is called with all input
    and output specified in decorator above
    """
    assert determine_if_tachy(age, HR) == expected

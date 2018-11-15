import pytest
from new_p import get_heart_rate
from validate_get_heart_rate import validate_get_heart_rate, ValidationError


def test_get_heart_rate_empty():
    n=[]
    with pytest.raises(ValidationError):
        validate_get_heart_rate(n)


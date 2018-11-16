class ValidationError(Exception):
    def __init__(self, message):
        self.message = message


def validate_get_heart_rate(HR):
    """
    Checks if there is HR data

    Args:
        HR (list): list of HR measurements

    Raises:
        ValidationError: no HR measurements
    """
    if len(HR) == 0:
        raise ValidationError("No heart rate data")

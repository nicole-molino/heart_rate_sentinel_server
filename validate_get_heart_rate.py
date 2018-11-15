class ValidationError(Exception):
    def __init__(self, message):
        self.message = message


def validate_get_heart_rate(HR):
    if len(HR) == 0:
        raise ValidationError("No heart rate data")


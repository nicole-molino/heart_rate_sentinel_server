from builtins import ValueError


def determine_if_tachy(age, HR):
    """
    Determine if patient is tachycardic

    Args:
        age (float): age of patient
        HR (float) : HR of patient

    Returns:
        a: connditional if tachy or not

    Raises:
        ValueError: patient younger than 2 months

    """
    a = 0
    if age < (1 / 12):
        raise ValueError("Age must be greater than 2 months")

    if age >= (1 / 12) and age < (3 / 12):
        if HR > 179:
            a = 1

    if age >= (3 / 12) and age <= (6 / 12):
        if HR > 186:
            a = 1

    if age >= (6 / 12) and age < 1:
        if HR > 169:
            a = 1

    if age >= 1 and age < 3:
        if HR > 151:
            a = 1

    if age >= 3 and age < 5:
        if HR > 137:
            a = 1

    if age >= 5 and age < 8:
        if HR > 133:
            a = 1

    if age >= 8 and age < 12:
        if HR > 130:
            a = 1

    if age >= 12 and age < 15:
        if HR > 119:
            a = 1

    if age >= 15:
        if HR > 100:
            a = 1

    return a

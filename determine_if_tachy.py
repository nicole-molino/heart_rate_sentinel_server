from builtins import ValueError


def determine_if_tachy(age, HR):
    if age < (1 / 12):
        raise ValueError("Age must be greater than 2 months. Retry")

    if age >= (1 / 12) and age < (3 / 12):
        if HR > 179:
            return 1
        else:
            return 0

    if age >= (3 / 12) and age <= (6 / 12):
        if HR > 186:
            return 1
        else:
            return 0

    if age >= (6 / 12) and age < 1:
        if HR > 169:
            return 1
        else:
            return 0

    if age >= 1 and age < 3:
        if HR > 151:
            return 1
        else:
            return 0

    if age >= 3 and age < 5:
        if HR > 137:
            return 1
        else:
            return 0

    if age >= 5 and age < 8:
        if HR > 133:
            return 1
        else:
            return 0

    if age >= 8 and age < 12:
        if HR > 130:
            return 1
        else:
            return 0

    if age >= 12 and age < 15:
        if HR > 119:
            return 1
        else:
            return 0

    if age >= 15:
        if HR > 100:
            return 1
        else:
            return 0

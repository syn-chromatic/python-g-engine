def clamp_float(value: float, min_value: float, max_value: float) -> float:
    return max(min(value, max_value), min_value)


def clamp_integer(value: int, min_value: int, max_value: int) -> int:
    return max(min(value, max_value), min_value)

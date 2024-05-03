from typing import List


def generate_equally_spaced_values(min_val: float = 0.1, max_val: float = 1, length: int = 10, invert: bool = False) -> List[float]:
    if invert:
        temp_max_val = min_val
        min_val = max_val
        max_val = temp_max_val
    step = (max_val - min_val) / (length - 1) if length > 1 else 0
    values = [round(min_val + i * step, 4) for i in range(length)]
    return values

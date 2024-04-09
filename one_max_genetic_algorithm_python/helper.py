from typing import List


def generate_equally_spaced_values(min_val: float = 0.1, max_val: float = 1, length: int = 10) -> List[float]:
    step = (max_val - min_val) / (length - 1)
    values = [round(min_val + i * step, 4) for i in range(length)]
    return values

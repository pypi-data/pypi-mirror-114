import math
from typing import Tuple


def float2frac(x: float, error: float = 1e-9) -> Tuple[int, int]:
    """Convert floating point to closest fraction

    Args:
        x (float): Floating-point number
        error (float, optional): Error bound. Defaults to 1e-9.

    Returns:
        Tuple[int, int]: Numerator, Denominator
    """
    n = int(math.floor(x))
    x -= n
    if x < error:
        return (n, 1)
    if 1 - error < x:
        return (n+1, 1)

    # The lower fraction is 0/1
    lower_n = 0
    lower_d = 1
    # The upper fraction is 1/1
    upper_n = 1
    upper_d = 1
    while True:
        # The middle fraction is (lower_n + upper_n) / (lower_d + upper_d)
        middle_n = lower_n + upper_n
        middle_d = lower_d + upper_d
        # If x + error < middle
        if middle_d * (x + error) < middle_n:
            # middle is our new upper
            upper_n = middle_n
            upper_d = middle_d
        # Else If middle < x - error
        elif middle_n < (x - error) * middle_d:
            # middle is our new lower
            lower_n = middle_n
            lower_d = middle_d
        # Else middle is our best fraction
        else:
            return n * middle_d + middle_n, middle_d

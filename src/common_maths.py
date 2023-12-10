from __future__ import annotations

from functools import lru_cache
from typing import Iterable

from common import multiply_together


# Thanks https://stackoverflow.com/questions/16996217/prime-factorization-list
@lru_cache(maxsize=None)
def prime_factors(number: int) -> list[int]:
    n: float = number
    f, fs = 3, []
    while n % 2 == 0:
        fs.append(2)
        n /= 2
    while f * f <= n:
        while n % f == 0:
            fs.append(int(f))
            n /= f
        f += 2
    if n > 1:
        fs.append(int(n))
    return fs


def smallest_common_multiple(numbers: Iterable[int]) -> int:
    factors = []
    for n in numbers:
        factors.extend(prime_factors(n))
    return multiply_together(set(factors))

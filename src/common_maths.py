from functools import lru_cache

primes: set[int] = set()


# Thanks https://stackoverflow.com/questions/15347174/python-finding-prime-factors
@lru_cache(maxsize=None)
def prime_factors(n: int):
    if n < 2:
        return [1]
    prime_factors(int(n**0.5))

    for prime in primes:
        if n % prime == 0:
            return sorted((prime, *prime_factors(n // prime)))

    primes.add(n)
    return [n]

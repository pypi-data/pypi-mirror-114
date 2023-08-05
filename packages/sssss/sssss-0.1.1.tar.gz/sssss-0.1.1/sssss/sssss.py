"""
The following Python implementation of Shamir's Secret Sharing is released into
the Public Domain under the terms of CC0 and OWFa:
https://creativecommons.org/publicdomain/zero/1.0/
http://www.openwebfoundation.org/legal/the-owf-1-0-agreements/owfa-1-0

Functions for static (deterministic) creation and reconstruction of secret shares.
"""

import random

_PRIME = (2**256)+297  # First prime after 2^256.


def _eval_at(poly, x, prime):
    """Evaluates polynomial (coefficient tuple) at x, used to generate a
    shamir pool in make_random_shares below.
    """
    accum = 0
    for coeff in reversed(poly):
        accum *= x
        accum += coeff
        accum %= prime
    return accum


def _extended_gcd(a, b):
    """
    Division in integers modulus p means finding the inverse of the
    denominator modulo p and then multiplying the numerator by this
    inverse (Note: inverse of A is B such that A*B % p == 1) this can
    be computed via extended Euclidean algorithm
    http://en.wikipedia.org/wiki/Modular_multiplicative_inverse#Computation
    """
    x = 0
    last_x = 1
    y = 1
    last_y = 0
    while b != 0:
        quot = a // b
        a, b = b, a % b
        x, last_x = last_x - quot * x, x
        y, last_y = last_y - quot * y, y
    return last_x, last_y


def _divmod(num, den, p):
    """Compute num / den modulo prime p

    To explain what this means, the return value will be such that
    the following is true: den * _divmod(num, den, p) % p == num
    """
    inv, _ = _extended_gcd(den, p)
    return num * inv


def _lagrange_interpolate(x, x_s, y_s, p):
    """
    Find the y-value for the given x, given n (x, y) points;
    k points will define a polynomial of up to kth order.
    """
    k = len(x_s)
    assert k == len(set(x_s)), "points must be distinct"
    def PI(vals):  # upper-case PI -- product of inputs
        accum = 1
        for v in vals:
            accum *= v
        return accum
    nums = []  # avoid inexact division
    dens = []
    for i in range(k):
        others = list(x_s)
        cur = others.pop(i)
        nums.append(PI(x - o for o in others))
        dens.append(PI(cur - o for o in others))
    den = PI(dens)
    num = sum([_divmod(nums[i] * den * y_s[i] % p, dens[i], p)
               for i in range(k)])
    return (_divmod(num, den, p) + p) % p


def share(secret, minimum, shares, prime=_PRIME):
    """
    Generates a random shamir pool for a given secret, returns share points.
    """
    random.seed(secret)#.to_bytes(32, 'big'))
    secret_int = int.from_bytes(secret, 'big')
    if minimum > shares:
        raise ValueError("Secret would be irrecoverable.")
    poly = [secret_int] + [random.randrange(prime - 1) for i in range(minimum - 1)]
    points = [
        (i, _eval_at(poly, i, prime))
        for i in range(1, shares + 1)
    ]
    points_bytes = [
        x.to_bytes(1, 'big') + y.to_bytes(32, 'big')
        for x, y in points
    ]
    return points_bytes


def reconstruct(shares, prime=_PRIME):
    """
    Recover the secret from share points
    (x, y points on the polynomial).
    """
    if len(shares) < 2:
        raise ValueError("need at least two shares")
    if not len(shares[0]) == 33:
        raise ValueError("need at least two shares")
    x_s, y_s = zip(*[
        (
            share[0],
            int.from_bytes(share[1:33], 'big')
        )
        for share in shares
    ])
    secret_int = _lagrange_interpolate(0, x_s, y_s, prime)
    return secret_int.to_bytes(32, 'big').decode('ascii')

# Create a simple Point class to represent the affine points.
from collections import namedtuple

Point = namedtuple("Point", "x y")

# The point at infinity (origin for the group law).
origin = 'Origin'

# Choose a particular curve and prime.  We assume that p > 3.
prime = 15733
a = 1
b = 3


def is_valid(point):
    """
    Determine whether we have a valid representation of a point
    on our curve.  We assume that the x and y coordinates
    are always reduced modulo p, so that we can compare
    two points for equality with a simple ==.
    """
    if point == origin:
        return True
    else:
        return (
                (point.y ** 2 - (point.x ** 3 + a * point.x + b)) % prime == 0 and
                0 <= point.x < prime and 0 <= point.y < prime)


def inv_mod_p(x):
    """
    Compute an inverse for x modulo p, assuming that x
    is not divisible by p.
    """
    if x % prime == 0:
        raise ZeroDivisionError("Impossible inverse")
    return pow(x, prime - 2, prime)


def ec_inv(point):
    """
    Inverse of the point P on the elliptic curve y^2 = x^3 + ax + b.
    """
    if point == origin:
        return point
    return Point(point.x, (-point.y) % prime)


def ec_add(point_p, point_q):
    """
    Sum of the points P and Q on the elliptic curve y^2 = x^3 + ax + b.
    """
    if not (is_valid(point_p) and is_valid(point_q)):
        raise ValueError("Invalid inputs")

    # Deal with the special cases where either P, Q, or P + Q is
    # the origin.
    if point_p == origin:
        result = point_q
    elif point_q == origin:
        result = point_p
    elif point_q == ec_inv(point_p):
        result = origin
    else:
        # Cases not involving the origin.
        if point_p == point_q:
            dydx = (3 * point_p.x ** 2 + a) * inv_mod_p(2 * point_p.y)
        else:
            dydx = (point_q.y - point_p.y) * inv_mod_p(point_q.x - point_p.x)
        x = (dydx ** 2 - point_p.x - point_q.x) % prime
        y = (dydx * (point_p.x - x) - point_p.y) % prime
        result = Point(x, y)

    # The above computations *should* have given us another point
    # on the curve.
    assert is_valid(result)
    return result


P = Point(6, 15)
Q = Point(8, 1267)
R = Point(2, 3103)
TwoP = ec_add(P, P)
ThreeP = ec_add(TwoP, P)
# Compute 4P two different ways.
assert ec_add(P, ThreeP) == ec_add(TwoP, TwoP)
# Check the associative law.
assert ec_add(P, ec_add(Q, R)) == ec_add(ec_add(P, Q), R)

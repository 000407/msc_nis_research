from sage.all import *
from sage.schemes.elliptic_curves.ell_point import EllipticCurvePoint
from random import randrange


class StegoEllipticCurve:
    def __init__(self, prime, a: int, b: int, key_p: int, generator_conf: tuple[int, int, bool] = (-1, -1, True)):
        self._generator = None
        self.prime = prime
        self.a = a
        self.b = b
        self.key_p = key_p

        self.curve = EllipticCurve(GF(prime), [a, b])
        self.set_generator(generator_conf[0], generator_conf[1], at_random=generator_conf[2])

    @property
    def generator(self):
        return self._generator

    @property
    def key_u(self):
        return self.key_p * self._generator

    def set_generator(self, x: int = 0, y: int = 0, at_random: bool = True) -> None:
        if at_random:
            gns = self.curve.gens()
            self._generator = gns[randrange(len(gns))]
            return

        if y ^ 2 == x ^ 3 + self.a * x + self.b:
            raise ValueError(f'Co-ordinates ({x}, {y}) does not appear to be on the curve!')

        self._generator = self.curve(x, y)

    def generate_points(self, key_recip_u: EllipticCurvePoint) -> list[tuple[int, int]]:
        scalar = self.key_p * key_recip_u
        sm_res = []

        point_int = scalar
        for x in range(scalar.xy()[0]):
            point_int = point_int + scalar  # TODO: Generator? Or scalar?

            xy = point_int.xy()

            sm_res.append((int(xy[0]), int(xy[1])))

        # print(f'scalar.x: {scalar.xy()[0]}')
        # print(sm_res)

        return sm_res


if __name__ == '__main__':
    sec_a = StegoEllipticCurve(101, 2, 3, 43)
    sec_b = StegoEllipticCurve(101, 2, 3, 31)

    p_a = sec_a.key_u
    p_b = sec_b.key_u

    print(sec_a.generate_points(p_b))
    print(sec_b.generate_points(p_a))

    exit()

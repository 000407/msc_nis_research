from collections import namedtuple
from sage.all import *




if __name__ == '__main__':
    # test()
    p = 0x89abcdef012345672718281831415926141424f7
    a = 0x37a5abccd277bce87632ff3d4780c009ebe41497
    b = 0x0dd8dabf725e2f3228e85f1ad78fdedf9328239e

    g = Point(0x8723947fd6a3a1e53510c07dba38daf0109fa120, 0x445744911075522d8c3c5856d4ed7acda379936f)

    c = EllipticCurve(p, a, b)

    print(scalar_multiply(c, g, 0x8723947fd6a3a1e53510c07dba38daf0109fa120))

    exit()

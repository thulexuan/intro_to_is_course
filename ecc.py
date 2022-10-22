import libnum
import random
from libnum import ecc


def gcd(a, b):
    while a != 0:
        a, b = b % a, a
    return b


def findModInverse(a, m):
    if a == 0:
        raise ZeroDivisionError("division by zero")
    if a < 0:
        # k ** -1 = p - (-k) ** -1  (mod p)
        return m - findModInverse(-a, m)
    # if gcd(a, m) != 1:
    #     return None
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m

    while v3 != 0:
        q = u3 // v3
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
    return u1 % m


def findModExp(base, e, mod):
    X = base
    E = e
    Y = 1
    while E > 0:
        if E % 2 == 0:
            X = (X * X) % mod
            E = E / 2
        else:
            Y = (X * Y) % mod
            E = E - 1
    return Y


def generate_coprime(phiN):
    while True:
        e = random.randint(0, phiN)

        if gcd(e, phiN) != 1:
            e = random.randint(0, phiN)
        else:
            break
    return e


def point_add(curve, point1, point2):
    p, a, b = curve
    if point1 is None:
        # 0 + point2 = point2
        return point2
    if point2 is None:
        # point1 + 0 = point1
        return point1
    x1, y1 = point1
    x2, y2 = point2
    if x1 == x2 and y1 != y2:
        # point1 + (-point1) = 0
        return None
    if x1 == x2:
        # point1 == point2.
        m = (3 * x1 * x1 + a) * findModInverse(2 * y1, p)
    else:
        # != point2.
        m = (y1 - y2) * findModInverse(x1 - x2, p)
    x3 = m * m - x1 - x2
    y3 = y1 + m * (x3 - x1)
    result = (x3 % p, -y3 % p)
    return result


def scalar_multiply(curve, k, point):
    p, a, b = curve
    c = ecc.Curve(a, b, p)
    result = None
    addend = point
    while k:
        if k & 1:
            # Add.
            result = point_add(curve, result, addend)
        # Double.
        addend = point_add(curve, addend, addend)
        k >>= 1
    assert c.check(result)
    return result


def generate_elliptic_curve(n_bit):   # Sinh đường cong elliptic với p là số nguyên tố n bits
    p, a, b = (0, 0, 0)
    p = libnum.generate_prime(n_bit)

    while ((4 * a ** 3 + 27 * b ** 2) % p == 0):
        a = generate_coprime(p - 1)
        b = generate_coprime(p - 1)
    print("ELLIPTIC CURVE y^2 = x^3 + %dx + %db (mod %d)" % (a, b, p))
    print("Some first points on curve:")
    print(find_points_in_range(1, 20, (p, a, b)))
    print("Order: ", find_curve_order((p, a, b)))
    return (p, a, b)


def find_points_in_range(start, end, curve):
    p, a, b = curve
    x = start
    points = []
    while True:
        val = ((x * x * x) + a * x + b) % p

        rtn = libnum.jacobi(val, p)

        if (rtn == 1):
            res = next(libnum.sqrtmod(val, {p: 1}))
            points.append((x, int(res)))
            points.append((x, int(p - res)))

        x = x + 1
        if (x == end or x == p):
            return points


def find_curve_order(curve):
    p, a, b = curve
    x = 1
    count = 0;
    while True:
        val = ((x * x * x) + a * x + b) % p
        if (val == 0):
            count = 1
        rtn = libnum.jacobi(val, p)

        if (rtn == 1):
            res = next(libnum.sqrtmod(val, {p: 1}))
            count += 2
        x = x + 1

        if (x == p):
            return count + 1


def find_order(point, curve):
    _point = point
    k = 1
    i = 1

    while i:
        k = k + 1
        if (_point == None):
            i = 0
        _point = point_add(curve, point, _point, )
    return k - 1


def gerenate_keys(curve):
    p, a, b = curve

    randX = len(find_points_in_range(1, 20, curve)) // 2

    g = find_points_in_range(1, 100, curve)[randX]

    n = find_order(g, curve)
    d = random.randint(1, n - 1)
    print("\nGENERATE KEY PAIR")
    print("Private key:")
    print("  d = %d" % d)
    Q = scalar_multiply(curve, d, g)
    print("Public key:")
    print("  Elliptic Curve (p, a, b) = (%d, %d, %d)" % (p, a, b))
    print("  Base point g = (%d, %d)" % (g))
    print("  Subgroup order n = %d" % (n))
    print("  Q = (%d, %d)" % (Q))

    private_key = d
    public_key = (g, n, Q)
    return private_key, public_key



if __name__ == '__main__':


    n_bit = 18
    curve = generate_elliptic_curve(n_bit)
    private_key, public_key = gerenate_keys(curve)



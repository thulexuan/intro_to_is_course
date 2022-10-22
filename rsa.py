import libnum
import random
import hashlib


def gcd(a, b):
    while a != 0:
        a, b = b % a, a
    return b


def findModInverse(a, m):  # Tính a^-1 mod m
    if gcd(a, m) != 1:
        return None
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m

    while v3 != 0:
        q = u3 // v3
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
    return u1 % m


def findModExp(b, n, m):   # Tính b^n mod m
    power = b
    x = 1
    while n > 0:
        if n % 2 == 0:
            power = (power * power) % m
            n = n / 2
        else:
            x = (power * x) % m
            n = n - 1
    return x


def generate_primes(n_bit):   # Sinh số nguyên tố n bits
    while True:
        p = libnum.generate_prime(n_bit)
        q = libnum.generate_prime(n_bit)

        if p == q:
            q = libnum.generate_prime(n_bit)
        else:
            break
    return p, q


def generate_e(phiN):   # Sinh số e
    while True:
        e = random.randint(0, phiN)
        if gcd(e, phiN) != 1:
            e = random.randint(0, phiN)
        else:
            break
    return e

def generate_keys(n_bit):
    p, q = generate_primes(n_bit)
    n = p * q
    phiN = (p - 1) * (q - 1)
    e = 65537
    d = findModInverse(e, phiN)
    """
    print("Public key")
    print("  (e,n): (%d, %d)" % (e, n))
    print("Private key")
    print("  (d,n): (%d, %d)\n" % (d, n))
    """

    return (e, d, n)


def hash(message):
    return int.from_bytes(hashlib.sha1(message).digest(), "big")


def encryption(message, n_bit):
    e, d, n = generate_keys(n_bit)
    m = hash(message)
    c = pow(m, e, n)
    _m = pow(c, d, n)

    print("\nENCRYPTION\n")
    print("Plaintext: %s" % (message))
    print("Hash plaintext: %s\n" % (m))

    print("Encrypt")
    print("Ciphertext c = m ^ e mod n = ", c)
    print("\nDecrypt")
    print("Plaintext: m = c ^ d mod n = ", _m)
    print("%s" % ("TRUE" if m == _m else "FALSE"))


if __name__ == '__main__':
    n_bit = 500
    message = b'lexuanthu'
    e,d,n = generate_keys(n_bit)
    encryption(message, n_bit)



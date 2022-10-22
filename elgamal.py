
import libnum
import random
import rsa
import hashlib

def hash(message):
    return int.from_bytes(hashlib.sha1(message).digest(), "big")

def generate_primes(n_bit):
    return libnum.generate_prime(n_bit)

def generate_coprime(phiN):
    while True:
        e = random.randint(0, phiN)
        if rsa.gcd(e, phiN) != 1:
            e = random.randint(0, phiN)
        else:
            break
    return e


def find_primitive_root(p):
    if p == 2:
        return 1
    p1 = 2
    p2 = (p - 1) // p1

    # test random g's until one is found that is a primitive root mod p
    while (1):
        g = random.randint(2, p - 1)
        # g is a primitive root if for all prime factors of p-1, p[i]
        # g^((p-1)/p[i]) (mod p) is not congruent to 1
        if not (pow(g, (p - 1) // p1, p) == 1):
            if not pow(g, (p - 1) // p2, p) == 1:
                return g


def generate_keys():
    print("------------------------------------")
    print("GENERATE KEY PAIR")
    p = generate_primes(n_bit)
    alpha = find_primitive_root(p)
    a = random.randint(1, (p - 1) // 2)
    beta = pow(alpha, a, p)
    print("Prime numbers:")
    print("   p: %d" % (p))
    print("Primitive root:")
    print("   α: %d" % (alpha))
    print("Private key:")
    print("   a: %d" % (a))
    print("Public key β = α ^ a mod p:")
    print("   β: %d" % (beta))

    print("\nPublic key (p, α, β):")
    print("   (%d, %d, %d)" % (p, alpha, beta))
    print("Private key a:")
    print("   %d" % (a))

    return (p, alpha, a, beta)


def encrypt(message, keys):
    p, alpha, a, beta = keys
    x = hash(message)
    k = generate_coprime(p - 1)
    print("------------------------------------")
    print("\nENCRYPTION\n")
    print("Plaintext = %s" % message)
    print("Hash plaintext: x = %s\n" % (x))
    print("Random k = %d" % k)

    y1 = pow(alpha, k, p)
    print(" y1 = x * β ^ k mod p = %d" % y1)

    y2 = (x * pow(beta, k, p)) % p
    print(" y2 = a^k mod p = %d" % y2)

    print("Ciphertext: (γ, δ) = (%d, %d)" % (y1, y2))
    return (y1, y2)


def decrypt(Ciphertext, keys, message):
    print("------------------------------------")
    print("\nDECRYPTION\n")
    x = hash(message)
    p, alpha, a, beta = keys
    y1, y2 = Ciphertext
    _x = (y2 * pow(pow(y1, a, p), p - 2, p)) % p

    print("Hash plaintext: %s" % (x))
    print("Decrypt = y2 * (y1 ^ -a) mod p = %d" % _x)
    print("Decrypt: %s" % ("SUCCESS" if _x == x else "FALSE"))


if __name__ == '__main__':

    n_bit = 512
    message = b'lexuanthu'
    keys = generate_keys()
    Ciphertext = encrypt(message, keys)
    decrypt(Ciphertext, keys, message)


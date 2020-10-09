import typing as tp


def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    """
    Encrypts plaintext using a Caesar cipher.

    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext = ""
    # PUT YOUR CODE HERE
    for i in plaintext:
        if i.isalpha():
            if i.isupper():
                k = 63
            else:
                k = 95
            c = ord(i) - k
            if c + shift <= 26:
                ciphertext += chr(c + shift +k)
            else:
                s = shift
                while c <= 26 and s > 0:
                    c += 1
                    s -= 1
                ciphertext += chr(1 + s + k)
        else:
            ciphertext += i 

    return ciphertext


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    """
    Decrypts a ciphertext using a Caesar cipher.

    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    plaintext = ""
    # PUT YOUR CODE HERE
    for i in ciphertext:
        if i.isalpha():
            if i.isupper():
                k = 63
            else:
                k = 95
            c = ord(i) - k
            if c - shift > 0:
                plaintext += chr(c - shift + k)
            else:
                s = shift
                while c > 0 and s > 0:
                    c -= 1
                    s -=1
                plaintext += chr(26 - s + k)
        else:
            plaintext += i
    return plaintext


def caesar_breaker_brute_force(ciphertext: str, dictionary: tp.Set[str]) -> int:
    """
    Brute force breaking a Caesar cipher.
    """
    best_shift = 0
    # PUT YOUR CODE HERE
    for d in dictionary:
        if len(d) == len(ciphertext):
            for shift in range(27):
                if decryot_caesar(ciphertext, shift) == d:
                    best_shift = shift
    return best_shift

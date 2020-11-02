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
    ciphertext=''
    for i in plaintext:
        if i.isalpha():
            if ord('Z') - shift < ord(i) <= ord('Z') or ord('z') - shift < ord(i) <= ord('z'):
                ciphertext += chr(ord(i) - 26 + shift)
            else:
                ciphertext += chr(ord(i) + shift)
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
    plaintext = ''
    for i in ciphertext:
        if i.isalpha():
            if ord('A') + shift > ord(i) >= ord('A') or ord('a') + shift > ord(i) >= ord('a'):
                plaintext += chr(ord(i) + 26 - shift)
            else:
                plaintext += chr(ord(i) - shift)
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
        for shift in range(26):
          if decrypt_caesar(ciphertext, shift) == d:
            best_shift = shift
    return best_shift

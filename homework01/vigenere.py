def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.

    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""
    # PUT YOUR CODE HERE
    t = 0
    s = []
    while t <= len(keyword) and len(s) < len(plaintext):
        if t < len(keyword):
            s.append(keyword[t].upper())
            t += 1
        else:
            s.append(keyword[0].upper())
            t = 1
    for i in range(len(plaintext)):
        if plaintext[i].isalpha():
            if plaintext[i].isupper():
                k = 63
            else:
                k = 95
            c = ord(plaintext[i]) - k 
            shift = ord(s[i]) - 65
            if c + shift <= 27:
                ciphertext += chr(c + shift + k)
            else:
                while c <= 26 and shift > 0:
                    c += 1
                    shift -= 1
                ciphertext += chr(1 + shift + k)
        else:
            ciphertext += plaintext[i]
    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.

    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""
    # PUT YOUR CODE HERE
    t = 0
    s = []
    while t <= len(keyword) and len(s) < len(ciphertext):
        if t < len(keyword):
            s.append(keyword[t].upper())
            t += 1
        else:
            s.append(keyword[0].upper())
            t = 1
    for i in range(len(ciphertext)):
        if ciphertext[i].isalpha():
            if ciphertext[i].isupper():
                k = 63
            else:
                k = 95
            c = ord(ciphertext[i]) - k
            shift = ord(s[i]) - 65
            if c - shift > 0:
                plaintext += chr(c - shift + k)
            else:
                while c > 0 and shift > 0:
                    c -= 1
                    shift -= 1
                plaintext += chr(26 - shift + k)
        else:
            plaintext += ciphertext[i]
    return plaintext

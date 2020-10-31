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
    t = 0
    s = []
    while t <= len(keyword) and len(s) < len(plaintext): #создание списка из ключей для каждой буквы ввода
        if t < len(keyword):
            s.append(keyword[t].upper())
            t += 1
        else:
            s.append(keyword[0].upper())
            t = 1
    for i in range(len(plaintext)):                          #перебор букв ввода и добавление зашифрованных элементов в вывод
        if plaintext[i].isalpha():
            shift = ord(s[i]) - 65
            if ord('Z') - shift < ord(plaintext[i]) <= ord('Z') or ord('z') - shift < ord(plaintext[i]) <= ord('z'):
                ciphertext += chr(ord(plaintext[i]) - 26 + shift)
            else:
                ciphertext += chr(ord(plaintext[i]) + shift)
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
    t = 0
    s = []
    while t <= len(keyword) and len(s) < len(ciphertext): #создание списка из ключей для каждой буквы ввода
        if t < len(keyword):
            s.append(keyword[t].upper())
            t += 1
        else:
            s.append(keyword[0].upper())
            t = 1
    for i in range(len(ciphertext)):                          #перебор букв ввода и добавление расшифрованных элементов в вывод
        if ciphertext[i].isalpha():
            shift = ord(s[i]) - 65
            if ord('A') + shift > ord(ciphertext[i]) >= ord('A') or ord('a') + shift > ord(ciphertext[i]) >= ord('a'):
                plaintext += chr(ord(ciphertext[i]) + 26 - shift)
            else:
                plaintext += chr(ord(ciphertext[i]) - shift)
        else:
            plaintext += ciphertext[i]
    return plaintext

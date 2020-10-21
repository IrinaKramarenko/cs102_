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
            if plaintext[i].isupper():
                shift_uni = 63
            else:
                shift_uni = 95
            letter1 = ord(plaintext[i]) - shift_uni
            shift = ord(s[i]) - 65
            if letter1 + shift <= 27:
                ciphertext += chr(letter1 + shift + shift_uni)
            else:
                while letter1 <= 26 and shift > 0:
                    letter1 += 1
                    shift -= 1
                ciphertext += chr(1 + shift + shift_uni)
        else:                                               #добавление небуквенных элементов в вывод
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
            if ciphertext[i].isupper():
                shift_uni = 63
            else:
                shift_uni = 95
            letter1 = ord(ciphertext[i]) - shift_uni
            shift = ord(s[i]) - 65
            if letter1 - shift > 0:
                plaintext += chr(letter1 - shift + shift_uni)
            else:
                while letter1 > 0 and shift > 0:
                    letter1 -= 1
                    shift -= 1
                plaintext += chr(26 - shift + shift_uni)
        else:                                         #добавление небуквенных элементов в вывод
            plaintext += ciphertext[i]
    return plaintext

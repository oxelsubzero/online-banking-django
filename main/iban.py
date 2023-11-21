import random


def generate_random_account() :
    acc = "1972"
    for _ in range(7):
        acc += str(random.randint(0,9))
    return acc

def generate_random_iban(country_code):
    country_code = country_code.upper()
    iban = country_code
    iban += '00'  # Ajoute deux chiffres de contrôle temporaires

    # Génère les 20 chiffres restants de manière aléatoire
    for _ in range(18):
        iban += str(random.randint(0, 9))

    # Calcule les chiffres de contrôle finaux en fonction de la spécification IBAN pour la France
    iban_digits = iban[4:]
    iban_digits += iban[0:4]

    iban_int = int(''.join(filter(str.isdigit, iban_digits)))  # Extrait uniquement les chiffres
    iban_check_digits = 97 - (iban_int % 97)
    iban_check_digits = str(iban_check_digits).zfill(2)

    # Remplace les chiffres de contrôle temporaires par les chiffres de contrôle réels
    iban = country_code + iban_check_digits + iban[6:]

    formatted_iban = ' '.join([iban[i:i+4] for i in range(0, len(iban), 4)])

    return formatted_iban



def generate_card():
    nb = "4"
    for _ in range(15):
        nb += str(random.randint(0,9))

    nb = ' '.join([nb[i:i+4] for i in range(0,len(nb),4)])
    
    cvv = ""
    for _ in range(3):
        cvv += str(random.randint(0,9))

    return [nb,cvv]

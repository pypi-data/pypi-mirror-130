character_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '+', '=']

def convert(value, to_base = 16, from_base = 10):
    # Characters (max. base64) (0-9, A-Z, a-z, +, =)
    global character_list

    # Turn value to decimal
    value = str(value)
    multiplier = 1
    i = 0
    values = []
    total = 0
    
    for character in reversed(value):
        if character_list.index(character) >= from_base:
            return print(f'Not all characters are base {from_base} characters.')
        values.append(character_list.index(character) * multiplier)
        i += 1
        multiplier = from_base ** i

    for number in values:
        total += number

    value = int(total)

    # Convert from base 10 to wanted base.
    
    # Finds the length of the output.
    # All output characters are zeros.
    multiplier = 0
    
    max_place = multiplier + 1
    while to_base ** multiplier <= value:
        max_place = multiplier + 1
        multiplier += 1

    converted = character_list[0] * max_place

    # Fills the output with proper values.
    for digit in range(len(converted)):
        converted = converted[:digit] + character_list[value // to_base ** (len(converted) - digit - 1)] + converted[digit + 1:]
        value -= (value // to_base ** (len(converted) - digit - 1)) * to_base ** (len(converted) - digit - 1)

    return converted


def base2(value, from_base = 10):
    to_base = 2
    # Characters (max. base64) (0-9, A-Z, a-z, +, =)
    global character_list

    # Turn value to decimal
    value = str(value)
    multiplier = 1
    i = 0
    values = []
    total = 0
    
    for character in reversed(value):
        if character_list.index(character) >= from_base:
            return print(f'Not all characters are base {from_base} characters.')
        values.append(character_list.index(character) * multiplier)
        i += 1
        multiplier = from_base ** i

    for number in values:
        total += number

    value = int(total)

    # Convert from base 10 to wanted base.
    
    # Finds the length of the output.
    # All output characters are zeros.
    multiplier = 0
    
    max_place = multiplier + 1
    while to_base ** multiplier <= value:
        max_place = multiplier + 1
        multiplier += 1

    converted = character_list[0] * max_place

    # Fills the output with proper values.
    for digit in range(len(converted)):
        converted = converted[:digit] + character_list[value // to_base ** (len(converted) - digit - 1)] + converted[digit + 1:]
        value -= (value // to_base ** (len(converted) - digit - 1)) * to_base ** (len(converted) - digit - 1)

    return converted


def base8(value, from_base = 10):
    to_base = 8
    # Characters (max. base64) (0-9, A-Z, a-z, +, =)
    global character_list

    # Turn value to decimal
    value = str(value)
    multiplier = 1
    i = 0
    values = []
    total = 0
    
    for character in reversed(value):
        if character_list.index(character) >= from_base:
            return print(f'Not all characters are base {from_base} characters.')
        values.append(character_list.index(character) * multiplier)
        i += 1
        multiplier = from_base ** i

    for number in values:
        total += number

    value = int(total)

    # Convert from base 10 to wanted base.
    
    # Finds the length of the output.
    # All output characters are zeros.
    multiplier = 0
    
    max_place = multiplier + 1
    while to_base ** multiplier <= value:
        max_place = multiplier + 1
        multiplier += 1

    converted = character_list[0] * max_place

    # Fills the output with proper values.
    for digit in range(len(converted)):
        converted = converted[:digit] + character_list[value // to_base ** (len(converted) - digit - 1)] + converted[digit + 1:]
        value -= (value // to_base ** (len(converted) - digit - 1)) * to_base ** (len(converted) - digit - 1)

    return converted


def base10(value, from_base = 16):
    # Characters (max. base64) (0-9, A-Z, a-z, +, =)
    global character_list

    # Turn value to decimal
    value = str(value)
    multiplier = 1
    i = 0
    values = []
    total = 0
    
    for character in reversed(value):
        if character_list.index(character) >= from_base:
            return print(f'Not all characters are base {from_base} characters.')
        values.append(character_list.index(character) * multiplier)
        i += 1
        multiplier = from_base ** i

    for number in values:
        total += number

    value = int(total)
    converted = value

    return converted


def base16(value, from_base = 10):
    to_base = 16
    # Characters (max. base64) (0-9, A-Z, a-z, +, =)
    global character_list

    # Turn value to decimal
    value = str(value)
    multiplier = 1
    i = 0
    values = []
    total = 0
    
    for character in reversed(value):
        if character_list.index(character) >= from_base:
            return print(f'Not all characters are base {from_base} characters.')
        values.append(character_list.index(character) * multiplier)
        i += 1
        multiplier = from_base ** i

    for number in values:
        total += number

    value = int(total)

    # Convert from base 10 to wanted base.
    
    # Finds the length of the output.
    # All output characters are zeros.
    multiplier = 0
    
    max_place = multiplier + 1
    while to_base ** multiplier <= value:
        max_place = multiplier + 1
        multiplier += 1

    converted = character_list[0] * max_place

    # Fills the output with proper values.
    for digit in range(len(converted)):
        converted = converted[:digit] + character_list[value // to_base ** (len(converted) - digit - 1)] + converted[digit + 1:]
        value -= (value // to_base ** (len(converted) - digit - 1)) * to_base ** (len(converted) - digit - 1)

    return converted


def base32(value, from_base = 10):
    to_base = 32
    # Characters (max. base64) (0-9, A-Z, a-z, +, =)
    global character_list

    # Turn value to decimal
    value = str(value)
    multiplier = 1
    i = 0
    values = []
    total = 0
    
    for character in reversed(value):
        if character_list.index(character) >= from_base:
            return print(f'Not all characters are base {from_base} characters.')
        values.append(character_list.index(character) * multiplier)
        i += 1
        multiplier = from_base ** i

    for number in values:
        total += number

    value = int(total)

    # Convert from base 10 to wanted base.
    
    # Finds the length of the output.
    # All output characters are zeros.
    multiplier = 0
    
    max_place = multiplier + 1
    while to_base ** multiplier <= value:
        max_place = multiplier + 1
        multiplier += 1

    converted = character_list[0] * max_place

    # Fills the output with proper values.
    for digit in range(len(converted)):
        converted = converted[:digit] + character_list[value // to_base ** (len(converted) - digit - 1)] + converted[digit + 1:]
        value -= (value // to_base ** (len(converted) - digit - 1)) * to_base ** (len(converted) - digit - 1)

    return converted


def base64(value, from_base = 10):
    to_base = 64
    # Characters (max. base64) (0-9, A-Z, a-z, +, =)
    global character_list

    # Turn value to decimal
    value = str(value)
    multiplier = 1
    i = 0
    values = []
    total = 0
    
    for character in reversed(value):
        if character_list.index(character) >= from_base:
            return print(f'Not all characters are base {from_base} characters.')
        values.append(character_list.index(character) * multiplier)
        i += 1
        multiplier = from_base ** i

    for number in values:
        total += number

    value = int(total)

    # Convert from base 10 to wanted base.
    
    # Finds the length of the output.
    # All output characters are zeros.
    multiplier = 0
    
    max_place = multiplier + 1
    while to_base ** multiplier <= value:
        max_place = multiplier + 1
        multiplier += 1

    converted = character_list[0] * max_place

    # Fills the output with proper values.
    for digit in range(len(converted)):
        converted = converted[:digit] + character_list[value // to_base ** (len(converted) - digit - 1)] + converted[digit + 1:]
        value -= (value // to_base ** (len(converted) - digit - 1)) * to_base ** (len(converted) - digit - 1)

    return converted


def characters(AZ_or_az, az_or_AZ, special_character_1, special_character_2):
    global character_list
    if AZ_or_az == 'AZ':
        AZ_or_az = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    if AZ_or_az == 'az':
        AZ_or_az = 'abcdefghijklmnopqrstuvwxyz'

    if az_or_AZ == 'AZ':
        az_or_AZ = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    if az_or_AZ == 'az':
        az_or_AZ = 'abcdefghijklmnopqrstuvwxyz'

    if AZ_or_az is az_or_AZ:
        AZ_or_az = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        az_or_AZ = 'abcdefghijklmnopqrstuvwxyz'
    character_list = list(f'0123456789{AZ_or_az}{az_or_AZ}{special_character_1}{special_character_2}')


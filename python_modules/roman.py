#!/usr/bin/env python3
"""
Module providing functions for roman numerals,\
for use with things such as yeast chromosome numbering.

ToDo:
- add roman class?
- More error checking handeling
"""
import re
LEXICON = {'M':1000, 'D':500, 'C':100, 'L':50, 'X':10, 'V':5, 'I':1}
SYMBOLS = ['I', 'V', 'X', 'L', 'C', 'D', 'M']
VALUES = [1, 5, 10, 50, 100, 500, 1000]

def roman_to_int(roman, strict=True):
    """Convert Roman numerals to integers"""
    if strict and not strict_roman(roman):
        raise ValueError("Bad Roman numeral: not strictly proper")
    elif not is_roman(roman):
        raise ValueError("Bad Roman numeral: not interpretable")

    roman = roman.upper()
    i = len(roman) - 1
    elements = []
    current_level = 1
    while i >= 0:
        letter = roman[i]
        if LEXICON[letter] == current_level:
            # Process additional numerals
            elements.append(current_level)
            neg = False

        elif LEXICON[letter] > current_level:
            # Process movement to next level of numeral
            current_level = LEXICON[letter]
            elements.append(current_level)
            neg = False

        else:
            # Process negative numerals
            if neg:
                raise ValueError("Bad Roman numeral: only a single consequative\
                                  subtraction is allowed")
            else:
                neg = True
                elements.append(-LEXICON[letter])

        i -= 1
    return sum(elements)

def int_to_roman(integer):
    """Convert integer to Roman numerals"""
    if not isinstance(integer, int):
        raise TypeError("Roman numerals can only represent integers")
    elif integer < 0:
        raise ValueError("Roman numerals do not support negative numbers")

    out = []
    remaining = integer
    for i in reversed(range(len(SYMBOLS))):
        out.extend(SYMBOLS[i] * (remaining // VALUES[i]))
        remaining %= VALUES[i]

        if i > 0 and '5' in str(VALUES[i]) and remaining >= VALUES[i] - VALUES[i - 1]:
            out.append(SYMBOLS[i - 1] + SYMBOLS[i])
            remaining -= VALUES[i] - VALUES[i - 1]

        elif i > 1 and remaining >= VALUES[i] - VALUES[i - 2]:
            out.append(SYMBOLS[i - 2] + SYMBOLS[i])
            remaining -= VALUES[i] - VALUES[i - 2]

    return ''.join(out)

def is_roman(numeral):
    """Check if an input string is an interpretable numeral.\
       This does not necessarily mean a well constructed one and \
       allows things such as XVVVIIIIII"""
    neg = False
    level = 1
    for num in reversed(str(numeral).upper()):
        if num in SYMBOLS:
            if LEXICON[num] == level:
                continue
            elif LEXICON[num] > level:
                level = LEXICON[num]
            elif neg:
                return False
            else:
                neg = True
        else:
            return False

    return True

def strict_roman(numeral):
    """Check if an input string is a well formated Roman numeral"""
    regexp = "M*(CM|DC{0,4}|CD|C{0,4})(XC|LX{0,4}|XL|X{0,4})(IX|VI{0,4}|IV|I{0,4})"
    return not re.fullmatch(regexp, str(numeral).upper()) is None

if __name__ == "__main__":
    print('Example functionality')
    print('roman_to_int("III") -> ', roman_to_int("III"))
    print('roman_to_int("XIV") -> ', roman_to_int("XIV"))
    print('roman_to_int("MMDCCXLIII") -> ', roman_to_int("MMDCCXLIII"))
    print('roman_to_int("ix") -> ', roman_to_int("ix"))
    print('roman_to_int("liV") -> ', roman_to_int("liV"))
    print('int_to_roman(1) -> ', int_to_roman(1))
    print('int_to_roman(23) -> ', int_to_roman(23))
    print('int_to_roman(4) -> ', int_to_roman(4))
    print('int_to_roman(9) -> ', int_to_roman(9))
    print('int_to_roman(90) -> ', int_to_roman(90))
    print('int_to_roman(2018) -> ', int_to_roman(2018))
    print('int_to_roman(194) -> ', int_to_roman(194))

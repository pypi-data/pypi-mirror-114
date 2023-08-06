#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
#    MusaMusa-RomanNumbers Copyright (C) 2012 suizokukan
#    Contact: suizokukan _A.T._ orange dot fr
#
#    This file is part of MusaMusa-RomanNumbers.
#    MusaMusa-RomanNumbers is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    MusaMusa-RomanNumbers is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with MusaMusa-RomanNumbers.  If not, see <http://www.gnu.org/licenses/>.
###############################################################################
"""
        MusaMusa-RomanNumbers by suizokukan (suizokukan AT orange DOT fr)

        Conversion between Roman numbers and Arabic numbers.

        Code largely inspired by Dive Into Python, see
        http://www.diveintopython3.net/ .
        ________________________________________________________________________

        (pimydoc)Integers and Roman numbers in this module
        ⋅ Only basic conversions are possible; result may be absurd for integers
        ⋅ greater than 3999. Please note that strings like IIII aren't valid.
        ⋅
        ⋅ Some examples:
        ⋅ 1 <-> (True, 'I')
        ⋅ 2 <-> (True, 'II')
        ⋅ 3 <-> (True, 'III')
        ⋅ 4 <-> (True, 'IV')
        ⋅ 5 <-> (True, 'V')
        ⋅ 6 <-> (True, 'VI')
        ⋅ 7 <-> (True, 'VII')
        ⋅ 8 <-> (True, 'VIII')
        ⋅ 9 <-> (True, 'IX')
        ⋅ 10 <-> (True, 'X')
        ⋅ 11 <-> (True, 'XI')
        ⋅ (...)
        ⋅ 18 <-> (True, 'XVIII')
        ⋅ 19 <-> (True, 'XIX')
        ⋅ 20 <-> (True, 'XX')
        ⋅ (...)
        ⋅ 49 <-> (True, 'XLIX')
        ⋅ (...)
        ⋅ 89 <-> (True, 'LXXXIX')
        ⋅ (...)
        ⋅ 99 <-> (True, 'XCIX')
        ⋅ (...)
        ⋅ 499 <-> (True, 'CDXCIX')
        ⋅ 500 <-> (True, 'D')
        ⋅ 501 <-> (True, 'DI')
        ⋅ (...)
        ⋅ 99 <-> (True, 'CMXCIX')
        ⋅ 1000 <-> (True, 'M')
        ⋅ (...)
        ⋅ 3999 <-> (True, 'MMMCMCXIX')
        ________________________________________________________________________

        functions:
        o from_roman()
        o to_roman()
"""
import re

from musamusa_errors.error_messages import MusaMusaError


ROMANNUMERALMAP = (('M', 1000),
                   ('CM', 900),
                   ('D', 500),
                   ('CD', 400),
                   ('C', 100),
                   ('XC', 90),
                   ('L', 50),
                   ('XL', 40),
                   ('X', 10),
                   ('IX', 9),
                   ('V', 5),
                   ('IV', 4),
                   ('I', 1))

ROMANNUMERALPATTERN = re.compile("^M{0,4}(CM|CD|D?C{0,3})"
                                 "(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$")


def from_roman(src):
    """
        from_roman() function

        Convert Roman numeral to an integer
        ________________________________________________________________________

        ARGUMENT:
        ▪ src : (str) the source string

        RETURNED VALUE : (bool)success
                         (int)result | (str)error message
    """
    # (pimydoc)error::RomanNumbers-ERRORID000
    # ⋅ A null string can't be converted into a Roman numeral.
    # ⋅
    # ⋅ By example, the following line...
    # ⋅     from_roman("")
    # ⋅ ... will raise this error.
    if not src:
        error = MusaMusaError()
        error.msgid = "RomanNumbers-ERRORID000"
        error.msg = "Can't convert a null string into a Roman numeral."
        return (False,
                error)

    # (pimydoc)error::RomanNumbers-ERRORID001
    # ⋅ Some strings aren't valid Roman numeral strings.
    # ⋅
    # ⋅ By example, the following line...
    # ⋅     from_roman("XLX")
    # ⋅ ... will raise this error.
    if not ROMANNUMERALPATTERN.search(src):
        error = MusaMusaError()
        error.msgid = "RomanNumbers-ERRORID001"
        error.msg = f"Invalid Roman numeral '{src}'"
        return (False,
                error)

    result = 0
    index = 0
    for numeral, integer in ROMANNUMERALMAP:
        while src[index:index+len(numeral)] == numeral:
            result += integer
            index += len(numeral)
    return (True, result)


def to_roman(src):
    """
        to_roman() function

        convert an integer to a Roman numeral
        ________________________________________________________________________

        ARGUMENT:
        ▪ src : (str) the integer to be converted

        RETURNED VALUE : (bool)success
                         (str)result | (str)error message
    """
    # (pimydoc)error::RomanNumbers-ERRORID003
    # ⋅ Only integers are accepted by the to_roman() function.
    # ⋅
    # ⋅ By example, the following line...
    # ⋅     to_roman(2.5)
    # ⋅ ... will raise this error.
    # ⋅
    # ⋅ By example, the following line...
    # ⋅     to_roman(2j)
    # ⋅ ... will raise this error.
    if not isinstance(src, int):
        error = MusaMusaError()
        error.msgid = "RomanNumbers-ERRORID003"
        error.msg = f"Can't convert {src} since it's not an integer (type(src)={type(src)})"
        return (False,
                error)

    # (pimydoc)error::RomanNumbers-ERRORID002
    # ⋅ An integer strictly inferior to 1 can't be converted into a Roman
    # ⋅ numbers string.
    # ⋅
    # ⋅ By example, the following line...
    # ⋅     to_roman("0")
    # ⋅ ... will raise this error.
    if src < 1:
        error = MusaMusaError()
        error.msgid = "RomanNumbers-ERRORID002"
        error.msg = f"Can't convert {src} since it's an integer smaller than 1"
        return (False,
                error)

    result = ""
    for numeral, integer in ROMANNUMERALMAP:
        while src >= integer:
            result += numeral
            src -= integer

    return (True, result)

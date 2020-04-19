#! /usr/bin/python3

import re


def get_base(lit):
    base = 1 if 'b' in lit else 8
    exp = 1024 if 'i' in lit else 1000

    if 'K' in lit:
        pow = 1
    elif 'M' in lit:
        pow = 2
    elif 'G' in lit:
        pow = 3
    elif 'T' in lit:
        pow = 4
    elif 'P' in lit:
        pow = 5
    else:
        pow = 0

    return base * exp ** pow


def split_literal(text):
    num_list = re.findall('^[0-9\.]+', text)
    return 1 if len(num_list) == 0 else float(num_list[0]), re.findall('[a-zA-Z]+$', text)[0]


class Filesize:

    PREFIX = ['', 'K', 'M', 'G', 'T', 'P']

    def __init__(self, a=0, b=None):
        if isinstance(a, str):
            a, b = split_literal(a)

        if b is None:
            b = ''

        self._bits = int(a * get_base(b))

    def floor(self, lit):
        return self._bits // get_base(lit)

    def round(self, lit, ndigits=None):
        if isinstance(lit, str):
            lit = get_base(lit)
        return round(self._bits / lit, ndigits)

    def show_iec_bytes(self):
        buff = self._bits // 8
        base = 8
        i = 0
        while buff >= 1024:
            buff = buff >> 10
            base = base << 10
            i += 1
        return str(self.round(base, 2)) + self.PREFIX[i] + 'iB'

    def show_iec_bits(self):
        buff = self._bits
        base = 1
        i = 0
        while buff >= 1024:
            buff = buff >> 10
            base = base << 10
            i += 1
        return str(self.round(base, 2)) + self.PREFIX[i] + 'ib'

    def show_si_bytes(self):
        buff = self._bits // 8
        base = 8
        i = 0
        while buff >= 1000:
            buff /= 1000
            base *= 1000
            i += 1
        return str(self.round(base, 2)) + self.PREFIX[i] + 'B'

    def show_si_bits(self):
        buff = self._bits
        base = 1
        i = 0
        while buff >= 1000:
            buff /= 1000
            base *= 1000
            i += 1
        return str(self.round(base, 2)) + self.PREFIX[i] + 'b'

    def __repr__(self):
        return self.show_iec_bytes()

    def __add__(self, value):
        if isinstance(value, Filesize):
            return Filesize(self._bits + value._bits, 'b')

        return self + Filesize(value)

    def __radd__(self, value):
        return Filesize(value) + self

    def __sub__(self, value):
        if isinstance(value, Filesize):
            return Filesize(self._bits - value._bits, 'b')

        return self - Filesize(value)

    def __rsub__(self, value):
        return Filesize(value) - self

    def __mul__(self, value):
        return Filesize(int(self._bits * value), 'b')

    def __rmul__(self, value):
        return Filesize(int(value * self._bits), 'b')

    def __div__(self, value):
        return Filesize(int(self._bits / value), 'b')

    def __floordiv__(self):
        return Filesize(int(self._bits // value), 'b')

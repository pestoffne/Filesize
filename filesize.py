#! /usr/bin/python3

import re


def get_base(lit):
    base = 1 if 'b' in lit else 8
    exp = 1024 if 'i' in lit else 1000

    for index, prefix in enumerate(Filesize.PREFIX):
        if prefix != '' and prefix in lit:
            power = index
            break
    else:
        power = 0

    return base * exp ** power


def split_literal(text):
    num_list = re.findall('^[0-9.]+', text)
    return 1 if len(num_list) == 0 else float(num_list[0]), re.findall('[a-zA-Z]+$', text)[0]


class Filesize:

    PREFIX     = ['',    'K',    'M',    'G',    'T',    'P',    'E',     'Z',     'Y']
    PREFIX_IEC = ['', 'kibi', 'mebi', 'gibi', 'tebi', 'pebi', 'exbi',  'zebi',  'yobi']
    PREFIX_SI  = ['', 'kilo', 'mega', 'giga', 'tera', 'peta',  'exa', 'zetta', 'yotta']
    MAX_PREFIX = len(PREFIX) - 1

    def __init__(self, a=0, b=None):
        if isinstance(a, str):
            a, b = split_literal(a)

        if b is None:
            b = ''

        self._bits = int(a * get_base(b))

        self.base = 8
        self.exp = 1024
        self.postfix = 'iB'
        self.prefixes = self.PREFIX
        self.ndigits = 2

    def floor(self, lit):
        return self._bits // get_base(lit)

    def round(self, lit, ndigits=None):
        if isinstance(lit, str):
            lit = get_base(lit)
        return round(self._bits / lit, ndigits)

    def _show(self, base, exp, postfix, prefixes, ndigits):
        buff = self._bits // base
        i = 0
        while buff >= exp:
            buff /= exp
            base *= exp
            i += 1
            if i >= self.MAX_PREFIX:
                break
        return str(self.round(base, ndigits)) + prefixes[i] + postfix

    def show(self, form=None):
        if 'iec' in form:
            exp = 1024
            postfix = 'iB'
        elif 'si' in form:
            exp = 1000
            postfix = 'B'
        else:
            exp = self.exp
            postfix = self.postfix

        ndigits_str = re.findall('[0-9]+', form)[0]
        ndigits = int(ndigits_str) if len(ndigits_str) >= 0 else None

        if form is None or len(form) == 0:
            base = self.base
        elif form[-1] == 'B':
            base = 8
        elif form[-1] == 'b':
            base = 1
        else:
            base = self.base

        return self._show(base, exp, postfix, self.prefixes, ndigits)

    def show_iec_bytes(self):
        return self._show(8, 1024, 'iB', self.PREFIX, 2)

    def show_iec_bits(self):
        return self._show(1, 1024, 'ib', self.PREFIX, 2)

    def show_si_bytes(self):
        return self._show(8, 1000, 'B', self.PREFIX, 2)

    def show_si_bits(self):
        return self._show(1, 1000, 'b', self.PREFIX, 2)

    def __repr__(self):
        return self._show(self.base, self.exp, self.postfix, self.prefixes)

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

    def __truediv__(self, value):
        return Filesize(int(self._bits / value), 'b')

    def __floordiv__(self, value):
        return Filesize(int(self._bits // value), 'b')

    def __lt__(self, value):
        assert isinstance(value, Filesize)
        return self._bits < value._bits

    def __le__(self, value):
        assert isinstance(value, Filesize)
        return self._bits <= value._bits

    def __gt__(self, value):
        assert isinstance(value, Filesize)
        return self._bits > value._bits

    def __ge__(self, value):
        assert isinstance(value, Filesize)
        return self._bits >= value._bits

    def __eq__(self, value):
        assert isinstance(value, Filesize)
        return self._bits == value._bits

    def __ne__(self, value):
        assert isinstance(value, Filesize)
        return self._bits != value._bits

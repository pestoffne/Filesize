#! /usr/bin/python3

from numpy import uint8, float32

from filesize import *


class TestFilesize:

    def setUp(self):
        pass

    def teardown(self):
        pass

    def test_get_base(self):
        assert get_base('Kb') == 1000
        assert get_base('Mb') == 1000 ** 2
        assert get_base('Gb') == 1000 ** 3
        assert get_base('Tb') == 1000 ** 4
        assert get_base('Pb') == 1000 ** 5

        assert get_base('Kib') == 1024
        assert get_base('Mib') == 1024 ** 2
        assert get_base('Gib') == 1024 ** 3
        assert get_base('Tib') == 1024 ** 4
        assert get_base('Pib') == 1024 ** 5

        assert get_base('KB') == 8 * 1000
        assert get_base('MB') == 8 * 1000 ** 2
        assert get_base('GB') == 8 * 1000 ** 3
        assert get_base('TB') == 8 * 1000 ** 4
        assert get_base('PB') == 8 * 1000 ** 5

        assert get_base('KiB') == 8 * 1024
        assert get_base('MiB') == 8 * 1024 ** 2
        assert get_base('GiB') == 8 * 1024 ** 3
        assert get_base('TiB') == 8 * 1024 ** 4
        assert get_base('PiB') == 8 * 1024 ** 5

        # no prefix
        assert get_base('b') == 1
        assert get_base('B') == 8

        # no unit
        assert get_base('K') == get_base('KB')
        assert get_base('M') == get_base('MB')
        assert get_base('G') == get_base('GB')
        assert get_base('T') == get_base('TB')
        assert get_base('P') == get_base('PB')

        assert get_base('Ki') == get_base('KiB')
        assert get_base('Mi') == get_base('MiB')
        assert get_base('Gi') == get_base('GiB')
        assert get_base('Ti') == get_base('TiB')
        assert get_base('Pi') == get_base('PiB')

        # no prefix and no unit
        assert get_base('') == 8

    def test_split_literal(self):
        assert split_literal('13579b') == (13579, 'b')
        assert split_literal('111GB') == (111, 'GB')
        assert split_literal('369MiB') == (369, 'MiB')
        assert split_literal('007 Pib') == (7, 'Pib')
        assert split_literal('PB') == (1, 'PB')
        assert split_literal('2.71828Gib') == (2.71828, 'Gib')

    def test_init(self):
        assert Filesize()._bits == 0
        assert Filesize('100B')._bits == 800
        assert Filesize(100, 'B')._bits == 800
        assert Filesize(100)._bits == 800
        assert Filesize('1KB')._bits == 8000

        assert Filesize('Kb')._bits == 1000
        assert Filesize(uint8(100), 'KB')._bits == 800_000

        assert Filesize(2.81, 'GiB').round('GiB', 2) == 2.81
        assert Filesize('117.43Mb').round('Mb', 2) == 117.43

    def test_floor(self):
        assert Filesize('1024KB').floor('KiB') == 1000

    def test_round(self):
        assert Filesize(1100).round('KB') == 1
        assert Filesize(1100).round('KB', 0) == 1
        assert Filesize(1100).round('KB', 1) == 1.1
        assert Filesize(1100).round('KB', 2) == 1.1
        assert Filesize(1100).round('KiB') == 1
        assert Filesize(1100).round('KiB', 2) == 1.07  # round(1100 / 1024, 2)
        assert Filesize(1111).round('B', -2) == 1100
        assert Filesize('2GB').round('GB') == 2
        assert Filesize(1100).round(8 * 1024, 2) == 1.07

    def test_add(self):
        assert (Filesize('2GB') + Filesize('2GB')).round('GB', 1) == 4.0
        assert (Filesize('GiB') + Filesize('GiB')).round('GiB', 1) == 2.0
        assert (Filesize('GiB') + Filesize('GiB') + Filesize('GiB')).round('GiB', 1) == 3.0
        assert (Filesize('2GB') + '2GB').round('GB', 1) == 4.0
        assert (Filesize('2GB') + '2GB' + '2GB').round('GB', 1) == 6.0
        assert (Filesize('1KB') + 80).round('B') == 1080
        assert (Filesize('1KiB') + 56).round('B') == 1080

    def test_radd(self):
        assert ('2GB' + Filesize('2GB')).round('GB', 1) == 4.0
        assert (56 + Filesize('1KiB')).round('B') == 1080

    def test_sub(self):
        assert (Filesize('Ki') - Filesize('K'))._bits == 8 * 24
        assert (Filesize('Ki') - 1000)._bits == 8 * 24
        assert (Filesize('Ki') - 'K')._bits == 8 * 24

    def test_rsub(self):
        assert (1024 - Filesize('K'))._bits == 8 * 24
        assert ('Ki' - Filesize('K'))._bits == 8 * 24

    def test_mul(self):
        assert (Filesize('512MiB') * 2).round('GiB', 2) == 1.0
        assert (Filesize('1GiB') * 0.5).round('GiB', 2) == 0.5

    def test_rmul(self):
        assert (0.5 * Filesize('1GiB')).round('GiB', 2) == 0.5

    def test_div(self):
        assert (Filesize('Gi') / 2).round('Mi', 2) == 512.0

    def test_floor_div(self):
        assert (Filesize('Gi') // 2).round('Mi', 2) == 512.0

    def test_check_types(self):
        assert isinstance((Filesize() * float32(0.3))._bits, int)
        assert isinstance(Filesize(uint8(8))._bits, int)

    def test_show_iec_bytes(self):
        assert Filesize('2.34GiB').show_iec_bytes() == '2.34GiB'

    def test_show_iec_bits(self):
        assert Filesize('1.23Mib').show_iec_bits() == '1.23Mib'

    def test_show_si_bytes(self):
        assert Filesize('2.22TB').show_si_bytes() == '2.22TB'

    def test_show_si_bits(self):
        assert Filesize('1.11Kb').show_si_bits() == '1.11Kb'

    def test_eq(self):
        assert (Filesize('1024K') == Filesize('1000Ki')) is True
        assert (Filesize(1) == Filesize(2)) is False

    def test_ne(self):
        assert (Filesize('1024K') != Filesize('1000Ki')) is False
        assert (Filesize(1) != Filesize(2)) is True

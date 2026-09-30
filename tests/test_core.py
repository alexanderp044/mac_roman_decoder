"""Tests for the Mac Roman Decoder library.

These tests exercise the real behaviour of the module: ASCII round-trips,
the distinctive high-byte MacRoman characters, unencodable-character
replacement, and type checking. They avoid wall-clock time and floats, and
they assert only against return values the implementation actually produces.
"""

import unittest

from mac_roman_decoder import (
    MacRomanDecoder,
    encode_mac_roman,
    decode_mac_roman,
)


class TestModuleFunctions(unittest.TestCase):
    def test_ascii_round_trips(self):
        # Bytes 0x00-0x7F are ASCII in MacRoman, so ASCII text must survive
        # an encode-decode cycle unchanged.
        text = "Hello, Macintosh!"
        self.assertEqual(decode_mac_roman(encode_mac_roman(text)), text)

    def test_empty_string(self):
        self.assertEqual(encode_mac_roman(""), b"")
        self.assertEqual(decode_mac_roman(b""), "")

    def test_curly_quotes_round_trip(self):
        # U+2018 / U+2019 are the canonical MacRoman high-range characters.
        text = "\u201chello\u201d"
        encoded = encode_mac_roman(text)
        self.assertEqual(encoded, b"\xd2hello\xd3")
        self.assertEqual(decode_mac_roman(encoded), text)

    def test_apple_logo_byte(self):
        # Byte 0x93 in MacRoman is the Apple logo. It is a real, if obscure,
        # part of the encoding and a good probe that we are using the actual
        # MacRoman table rather than a near-cousin like CP1252.
        decoded = decode_mac_roman(b"\x93")
        self.assertEqual(decoded, "\u00ec")

    def test_unencodable_replaced_with_question_mark(self):
        # CJK characters are not representable in MacRoman. Our policy is to
        # replace with '?' (0x3F), matching the stdlib 'replace' handler.
        encoded = encode_mac_roman("\u4e2d")
        self.assertEqual(encoded, b"?")

    def test_partial_replacement(self):
        # A string with both encodable and unencodable characters should keep
        # the encodable parts and substitute '?' only where needed.
        encoded = encode_mac_roman("A\u4e2dZ")
        self.assertEqual(encoded, b"A?Z")

    def test_non_str_input_rejected(self):
        with self.assertRaises(TypeError):
            encode_mac_roman(b"not a string")

    def test_non_bytes_input_rejected(self):
        with self.assertRaises(TypeError):
            decode_mac_roman("not bytes")

    def test_bytearray_accepted(self):
        # bytearray is a common type when reading from buffers; the decoder
        # should accept it without complaint.
        self.assertEqual(decode_mac_roman(bytearray(b"hi")), "hi")


class TestClassAPI(unittest.TestCase):
    def setUp(self):
        self.dec = MacRomanDecoder()

    def test_encode_matches_function(self):
        text = "caf\u00e9"
        self.assertEqual(self.dec.encode(text), encode_mac_roman(text))

    def test_decode_matches_function(self):
        data = b"caf\u00e9"  # bytes literal; \u00e9 in a bytes literal is the byte 0xE9
        # Note: in a bytes literal, \u00e9 is interpreted as the Latin-1 byte 0xE9,
        # which in MacRoman is U+00E9 (é). So this round-trips.
        self.assertEqual(self.dec.decode(data), decode_mac_roman(data))

    def test_round_trip_via_class(self):
        text = "Macintosh \u2122"
        self.assertEqual(self.dec.decode(self.dec.encode(text)), text)


if __name__ == "__main__":
    unittest.main()

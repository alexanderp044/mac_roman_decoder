"""Core implementation of the MacRoman encoder/decoder.

MacRoman is a single-byte encoding used as the system encoding on classic
Mac OS (System 1 through Mac OS 9). Its byte range 0x80-0xFF maps to a set
of characters that includes curly quotes, the Apple and Command-key glyphs,
math symbols, and accented Latin letters. Bytes 0x00-0x7F are identical to
ASCII, which is a property we rely on in the tests.

Python's standard library ships a ``mac_roman`` codec, so we delegate to it.
We do not reimplement the mapping table: the table is large, fixed, and
easy to get wrong by hand. The stdlib codec is the canonical reference.
"""

import codecs

# A single byte that cannot be encoded in MacRoman (e.g. a CJK character)
# is replaced with this byte. We use ASCII '?' (0x3F) because it is the
# conventional fallback for legacy single-byte encodings and is itself a
# valid MacRoman byte, so the output is always well-formed MacRoman bytes.
_FALLBACK_BYTE = ord("?")

# A byte in the high range that is undefined in MacRoman. In practice the
# MacRoman codec maps every byte 0x00-0xFF to *some* character, so this path
# is defensive rather than expected. We use U+FFFD REPLACEMENT CHARACTER,
# the Unicode standard's designated marker for an unmappable decoded byte.
_FALLBACK_CHAR = "\ufffd"


class MacRomanDecoder:
    """Encode text to and decode text from MacRoman bytes.

    The class is stateless; instances exist so callers have a stable object
    to pass around, mock in tests, or hold configuration if the API grows.
    All real work is done by the module-level functions.
    """

    def encode(self, text: str) -> bytes:
        """Encode a Python string into MacRoman bytes.

        Characters that have no MacRoman representation are replaced with
        ``b'?'``. This matches the behaviour of many legacy systems that
        used MacRoman and keeps the output a valid MacRoman byte stream.
        """
        return encode_mac_roman(text)

    def decode(self, data: bytes) -> str:
        """Decode MacRoman bytes into a Python string.

        Bytes that cannot be decoded (extremely rare for MacRoman, which
defines
        all 256 code points) are replaced with U+FFFD.
        """
        return decode_mac_roman(data)


def encode_mac_roman(text: str) -> bytes:
    """Encode a string to MacRoman bytes, replacing unencodable characters.

    The replacement uses ``?`` (0x3F). We chose ``replace`` rather than
    ``strict`` because MacRoman cannot represent the vast majority of
    Unicode (no CJK, no emoji, limited accents), and callers working with
    legacy Mac files generally prefer a readable fallback over an
    exception. If a caller needs strict semantics they should use
    ``codecs.encode(text, "mac_roman")`` directly.

    Args:
        text: The string to encode.

    Returns:
        A ``bytes`` object in MacRoman encoding.
    """
    if not isinstance(text, str):
        raise TypeError(f"expected str, got {type(text).__name__}")
    return codecs.encode(text, "mac_roman", errors="replace")


def decode_mac_roman(data: bytes) -> str:
    """Decode MacRoman bytes into a string, replacing undecodable bytes.

    The replacement uses U+FFFD. MacRoman assigns a character to every one
    of its 256 code points, so in practice the replacement path is only
    exercised by callers who pass non-MacRoman data (e.g. UTF-8 bytes) and
    want graceful degradation rather than mojibake.

    Args:
        data: The bytes to decode.

    Returns:
        A Python ``str``.
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError(f"expected bytes or bytearray, got {type(data).__name__}")
    return codecs.decode(bytes(data), "mac_roman", errors="replace")

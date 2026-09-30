"""Mac Roman Decoder: encode and decode the classic Mac OS character set.

This package exposes a small, dependency-free API for converting between
Python ``str`` objects and ``bytes`` in the MacRoman encoding (what Python's
standard library calls ``mac_roman``). The standard library's codecs already
support this encoding; this library wraps them with explicit, tested error
handling and a convenient class-based interface, rather than reimplementing
the 256-entry mapping table by hand.

Design choice: we delegate to the stdlib codec for the actual byte-by-byte
mapping rather than maintaining our own table. The table is fixed by the
encoding's definition; hand-copying it would only introduce transcription
errors and drift from the canonical mapping. The value we add is a tested
error-handling policy (replacement byte/character on invalid input) and a
class API that is easy to stub in tests.
"""

from .core import MacRomanDecoder, encode_mac_roman, decode_mac_roman

__all__ = [
    "MacRomanDecoder",
    "encode_mac_roman",
    "encode_mac_roman",
    "decode_mac_roman",
]

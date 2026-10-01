# Mac Roman Decoder

A small, dependency-free Python library for encoding and decoding text in the MacRoman character set, the default encoding of classic Mac OS.

## Usage

```python
from mac_roman_decoder import MacRomanDecoder, encode_mac_roman, decode_mac_roman

# Functional API
encoded = encode_mac_roman("“café”")   # b'\xd2caf\xe9\xd3'
decoded = decode_mac_roman(b'\xd2caf\xe9\xd3')  # '“café”'

# Class API
dec = MacRomanDecoder()
dec.encode("“café”")   # b'\xd2caf\xe9\xd3'
dec.decode(b'\xd2caf\xe9\xd3')  # '“café”'
```

## Why this exists

MacRoman is the system encoding of classic Mac OS. Files created on System 1 through Mac OS 9 — and some early Mac OS X Carbon applications — use it for filenames, text clippings, resource forks, and plain-text documents. When you need to read that data on a modern system, Python's standard library can handle the mapping, but its raw codec API is awkward and its error handling is strict by default.

This library wraps the standard `mac_roman` codec with a tested, lenient error policy: unencodable characters become `?` (0x3F) and undecodable bytes become U+FFFD. The mapping table itself is delegated to the stdlib codec rather than hand-copied, because the table is fixed and transcription errors are the most common way a reimplementation goes wrong.

## Edge cases

- Characters outside MacRoman's repertoire (CJK, emoji, most symbols beyond Latin-1 plus the Mac-specific block) are replaced with `?` on encode. There is no lossless fallback.
- MacRoman defines all 256 bytes, so decode rarely produces U+FFFD unless you feed it non-MacRoman bytes (e.g. UTF-8).
- The class is stateless; it exists for API symmetry and ease of mocking in tests.

## Exports

- `MacRomanDecoder` — class with `encode(text: str) -> bytes` and `decode(data: bytes) -> str`.
- `encode_mac_roman(text: str) -> bytes` — module-level encoder.
- `decode_mac_roman(data: bytes) -> str` — module-level decoder.

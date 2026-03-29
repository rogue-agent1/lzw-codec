#!/usr/bin/env python3
"""lzw_codec: LZW compression/decompression."""
import sys

def compress(data):
    if not data: return []
    dict_size = 256
    dictionary = {bytes([i]): i for i in range(256)}
    w = bytes([data[0]])
    result = []
    for c in data[1:]:
        cb = bytes([c]) if isinstance(c, int) else c.encode()
        wc = w + cb
        if wc in dictionary:
            w = wc
        else:
            result.append(dictionary[w])
            dictionary[wc] = dict_size
            dict_size += 1
            w = cb
    result.append(dictionary[w])
    return result

def decompress(codes):
    if not codes: return b""
    dict_size = 256
    dictionary = {i: bytes([i]) for i in range(256)}
    w = dictionary[codes[0]]
    result = bytearray(w)
    for code in codes[1:]:
        if code in dictionary:
            entry = dictionary[code]
        elif code == dict_size:
            entry = w + bytes([w[0]])
        else:
            raise ValueError(f"Bad code: {code}")
        result.extend(entry)
        dictionary[dict_size] = w + bytes([entry[0]])
        dict_size += 1
        w = entry
    return bytes(result)

def test():
    data = b"TOBEORNOTTOBEORTOBEORNOT"
    codes = compress(data)
    assert len(codes) < len(data)
    assert decompress(codes) == data
    # Single byte
    assert decompress(compress(b"A")) == b"A"
    # Repeated
    data2 = b"AAAAAAAAAA"
    assert decompress(compress(data2)) == data2
    # Empty
    assert compress(b"") == []
    assert decompress([]) == b""
    # All bytes
    data3 = bytes(range(256))
    assert decompress(compress(data3)) == data3
    print("All tests passed!")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test": test()
    else: print("Usage: lzw_codec.py test")

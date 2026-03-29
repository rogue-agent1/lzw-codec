#!/usr/bin/env python3
"""lzw_codec - LZW compression and decompression."""
import sys

def compress(data):
    if not data: return []
    dict_size = 256
    dictionary = {bytes([i]): i for i in range(dict_size)}
    if isinstance(data, str): data = data.encode()
    w = bytes([data[0]])
    result = []
    for c in data[1:]:
        wc = w + bytes([c])
        if wc in dictionary:
            w = wc
        else:
            result.append(dictionary[w])
            dictionary[wc] = dict_size
            dict_size += 1
            w = bytes([c])
    result.append(dictionary[w])
    return result

def decompress(codes):
    if not codes: return b""
    dict_size = 256
    dictionary = {i: bytes([i]) for i in range(dict_size)}
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
    assert decompress(compress(b"AAAAAAA")) == b"AAAAAAA"
    assert decompress(compress(b"")) == b""
    assert decompress(compress(b"A")) == b"A"
    big = b"abcdef" * 100
    assert decompress(compress(big)) == big
    print("lzw_codec: all tests passed")

if __name__ == "__main__":
    test() if "--test" in sys.argv else print("Usage: lzw_codec.py --test")

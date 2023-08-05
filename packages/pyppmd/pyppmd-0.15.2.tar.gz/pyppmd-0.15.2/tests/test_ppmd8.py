import hashlib
import os
import pathlib

import pyppmd

testdata_path = pathlib.Path(os.path.dirname(__file__)).joinpath("data")
source = b"This file is located in a folder.This file is located in the root.\n"
encoded = (
    b"\x54\x16\x43\x6d\x5c\xd8\xd7\x3a\xb3\x58\x31\xac\x1d\x09\x23\xfd\x11\xd5\x72\x62\x73"
    b"\x13\xb6\xce\xb2\xe7\x6a\xb9\xf6\xe8\x66\xf5\x08\xc3\x0a\x09\x36\x123B\x9a\xf7\x94\xda"
)
READ_BLOCKSIZE = 16384


def test_ppmd8_encoder1():
    encoder = pyppmd.Ppmd8Encoder(6, 8 << 20)
    result = encoder.encode(source)
    result += encoder.flush()
    assert result == encoded


def test_ppmd8_encoder2():
    encoder = pyppmd.Ppmd8Encoder(6, 8 << 20)
    result = encoder.encode(source[:33])
    result += encoder.encode(source[33:])
    result += encoder.flush()
    assert result == encoded


def test_ppmd8_decoder1():
    decoder = pyppmd.Ppmd8Decoder(6, 8 << 20)
    result = decoder.decode(encoded, -1)
    assert decoder.eof
    assert not decoder.needs_input
    assert result == source


def test_ppmd8_decoder2():
    decoder = pyppmd.Ppmd8Decoder(6, 8 << 20)
    result = decoder.decode(encoded[:20])
    result += decoder.decode(encoded[20:])
    assert not decoder.needs_input
    assert decoder.eof
    assert result == source


def test_ppmd8_encode_decode(tmp_path):
    length = 0
    m = hashlib.sha256()
    with testdata_path.joinpath("10000SalesRecords.csv").open("rb") as f:
        with tmp_path.joinpath("target.ppmd").open("wb") as target:
            enc = pyppmd.Ppmd8Encoder(6, 8 << 20)
            data = f.read(READ_BLOCKSIZE)
            while len(data) > 0:
                m.update(data)
                length += len(data)
                target.write(enc.encode(data))
                data = f.read(READ_BLOCKSIZE)
            target.write(enc.flush())
    shash = m.digest()
    m2 = hashlib.sha256()
    assert length == 1237262
    length = 0
    with tmp_path.joinpath("target.ppmd").open("rb") as target:
        with tmp_path.joinpath("target.csv").open("wb") as out:
            dec = pyppmd.Ppmd8Decoder(6, 8 << 20)
            data = target.read(READ_BLOCKSIZE)
            while len(data) > 0 or not dec.eof:
                res = dec.decode(data)
                m2.update(res)
                out.write(res)
                length += len(res)
                data = target.read(READ_BLOCKSIZE)
    assert length == 1237262
    thash = m2.digest()
    assert thash == shash

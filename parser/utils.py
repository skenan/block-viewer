import hashlib
import struct
import base58
from binascii import hexlify, unhexlify
from datetime import datetime


def btc_ripemd160(data):
    h1 = hashlib.sha256(data).digest()
    r160 = hashlib.new("ripemd160")
    r160.update(h1)
    return r160.digest()


def double_sha256(data):
    return hashlib.sha256(hashlib.sha256(data).digest()).digest()


def hash_to_address(pubkey_hash, is_p2sh=False):
    prefix = "00" if not is_p2sh else "05"
    extend_hash = unhexlify(prefix + pubkey_hash)
    checksum = double_sha256(extend_hash)
    return base58.b58encode(extend_hash + checksum[:4]).decode('utf-8')


def key_to_address(pubkey):
    key = unhexlify(pubkey)
    pubkey_hash = btc_ripemd160(key)
    extend_hash = b'\x00' + pubkey_hash
    checksum = double_sha256(extend_hash)
    return base58.b58encode(extend_hash + checksum[:4]).decode('utf-8')


def uint1(stream):
    return ord(stream.read(1))


def uint2(stream):
    return struct.unpack('H', stream.read(2))[0]


def uint4(stream):
    return struct.unpack('I', stream.read(4))[0]


def uint8(stream):
    return struct.unpack('Q', stream.read(8))[0]


def hash32(stream):
    return format_hash(stream.read(32)[::-1])


def time(stream):
    return decode_time(uint4(stream))


def varint(stream):
    size = uint1(stream)
    if size < 0xfd:
        return size
    if size == 0xfd:
        return uint2(stream)
    if size == 0xfe:
        return uint4(stream)
    if size == 0xff:
        return uint8(stream)
    return -1


def format_hash(bytebuffer):
    return str(hexlify(bytebuffer).decode("utf-8"))


def decode_time(input_time):
    utc_time = datetime.utcfromtimestamp(input_time)
    return utc_time.strftime("%Y-%m-%d %H:%M:%S")


def calc_difficulty(nBits):
    nShift = (nBits >> 24) & 0xff
    dDiff = float(0x0000ffff) / float(nBits & 0x00ffffff)
    while nShift < 29:
        dDiff *= 256.0
        nShift += 1
    while nShift > 29:
        dDiff /= 256.0
        nShift -= 1
    return dDiff

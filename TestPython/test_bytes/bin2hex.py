import base64
import binascii
import binhex
bin_ = bin(10)

binary_ = bytes('ah10', 'ascii')
print(binary_)

hex_1 = binascii.hexlify(binary_)
print(hex_1)

bin_1 = binascii.unhexlify(hex_1)
print(bin_1)

# bytearray.fromhex()


#  or

hex_2 = bytes.hex(binary_)
print(hex_2)

bin_2 = bytes(hex_2.encode('ascii'))
print(bin_2)


# This module encodes and decodes files in binhex4 format, a format allowing representation of Macintosh files in ASCII.
#  Only the data fork is handled.
# hex_2 = binhex.BinHex(binary_)
# print(hex_2)
#
# bin_ = binhex.HexBin(hex_2)
# print(bin_)

base64.encode()
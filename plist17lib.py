# Copyright 2023, Hendrik Wingbermuehle, Denys Serdyukov
# Based on https://github.com/python/cpython/blob/3.11/Lib/plistlib.py

from plistlib import InvalidFileException, _undefined, PlistFormat
from plistlib import load as plistlibLoad
import struct
from io import BytesIO

__all__ = [
    "_BinaryPlist17Parser"
]

class _BinaryPlist17Parser:
    """
    Read or write a bplist17 file.
    Raise InvalidFileException in case of error, otherwise return the
    root object.
    """

    def __init__(self, dict_type):
        self._dict_type = dict_type

    def parse(self, fp):
        try:
            # The basic file format:
            # MAGIC (6 bytes)
            # VERSION (2 bytes)
            
            # ROOT Object
            
            self._fp = fp
            # self._fp.seek(-32, os.SEEK_END)
            self._fp.seek(0)
            magic = self._fp.read(0x6)
            # print(magic)
            version = self._fp.read(0x2)
            # print(version)

            return self._read_object_at(0x8)

        except (OSError, IndexError, struct.error, OverflowError,
                ValueError):
            raise InvalidFileException()

    # def _get_size(self, tokenL):
    #     """ return the size of the next object."""
    #     if tokenL == 0xF:
    #         m = self._fp.read(1)[0] & 0x3
    #         s = 1 << m
    #         f = '>' + _BINARY_FORMAT[s]
    #         return struct.unpack(f, self._fp.read(s))[0]

    #     return tokenL

    # def _read_ints(self, n, size):
    #     data = self._fp.read(size * n)
    #     if size in _BINARY_FORMAT:
    #         return struct.unpack(f'>{n}{_BINARY_FORMAT[size]}', data)
    #     else:
    #         if not size or len(data) != size * n:
    #             raise InvalidFileException()
    #         return tuple(int.from_bytes(data[i: i + size], 'big')
    #                      for i in range(0, size * n, size))

    # def _read_refs(self, n):
    #     return self._read_ints(n, self._ref_size)

    def _read_object_at(self, addr):
        """
        read the object by reference.

        May recursively read sub-objects (content of an array/dict/set)
        """
        # print("Entered _read_object_at: ", addr)
        totalReadBytes = []
        self._fp.seek(addr)
        token = self._fp.read(1)[0]
        totalReadBytes.append(token)
        tokenH, tokenL = token & 0xF0, token & 0x0F

        # elif token == 0x0f:
        #     result = b''

        if tokenH == 0x10:  # int
            # Integer (length tokenL)
            result = int.from_bytes(self._fp.read(tokenL), 'big')

        elif token == 0x22: # real
            result = struct.unpack('<f', self._fp.read(4))[0]

        elif token == 0x23: # real
            result = struct.unpack('<d', self._fp.read(8))[0]

        elif tokenH == 0x40:  # data
            size = self._read_dynamic_size(totalReadBytes, tokenL)
            bytesData = self._fp.read(size)
            
            nestedData = BytesIO(bytesData)

            nestedData.seek(0)
            magic = nestedData.read(0x6)
            # print(magic)
            version = nestedData.read(0x2)
            # print(version)
            nestedData.seek(0)
            
            if len(bytesData) != size:
                raise InvalidFileException()
            
            result = ''.join('{:02x}'.format(x) for x in bytesData)
            
            if magic == b'bplist':
                if version == b'00':
                    # parse bplist00
                    #TODO Fix BPlist00 parser
                    # result = plistlibLoad(nestedData, fmt=PlistFormat.FMT_XML)
                    result = result
                elif version == b'17':
                    result = _BinaryPlist17Parser(dict).parse(nestedData)

        elif tokenH == 0x60:  # unicode string
            size = self._read_dynamic_size(totalReadBytes, tokenL) * 2
            data = self._fp.read(size)
            if len(data) != size:
                raise InvalidFileException()
            result = data.decode('utf-16le')
        
        elif tokenH == 0x70:  # ascii string
            size = self._read_dynamic_size(totalReadBytes, tokenL)
            data = self._fp.read(size)
            if len(data) != size:
                raise InvalidFileException()
            result = data.decode('ascii').rstrip('\x00')

        elif tokenH == 0x80:  # Referenced Object
            size = self._read_dynamic_size(totalReadBytes, tokenL)
            address = int.from_bytes(self._fp.read(size), 'little')
            currentAddr = self._fp.tell()
            result = self._read_object_at(address)
            self._fp.seek(currentAddr)


        elif tokenH == 0xA0:  # array
            endAddress = int.from_bytes(self._fp.read(0x8), 'little')
            result = []
            while(self._fp.tell() <= endAddress):
                result.append(self._read_object_at(self._fp.tell()))
            
            if self._fp.tell() != (endAddress + 1):
                raise InvalidFileException() # TODO: Descriptive Exception

        elif token == 0xB0: 
            result = True

        elif token == 0xC0:
            result = False

        elif tokenH == 0xD0:  # dict
            endAddress = int.from_bytes(self._fp.read(0x8), 'little')
            result = self._dict_type()
            try:
                while(self._fp.tell() <= endAddress):
                    key = self._read_object_at(self._fp.tell())
                    value = self._read_object_at(self._fp.tell())
                    result[key] = value
            except TypeError:
                raise InvalidFileException()
            
            if self._fp.tell() != (endAddress + 1):
                raise InvalidFileException() # TODO: Descriptive Exception
        
        elif token == 0xE0:
            result = None

        elif tokenH == 0xF0:
            result = int.from_bytes(self._fp.read(tokenL), 'big', signed=False)

        else:
            # raise InvalidFileException()
            raise TypeError("unsupported type: %s at: %s" % (''.join('{:02x}'.format(x) for x in totalReadBytes), addr))

        return result

    def _read_dynamic_size(self, totalReadBytes, tokenL):
        if tokenL == 0xF:
            token2 = self._fp.read(1)[0]
            totalReadBytes.append(token2)
            length = token2 & 0xF # extract last 4 bits from token2 as length
            if length != 0 and ((token2 & 0xF0) == 0x10) :
                size = int.from_bytes(self._fp.read(length), 'little')
            else:
                raise TypeError("unsupported type: %s" % ''.join('{:02x}'.format(x) for x in totalReadBytes))
        else:
            size = tokenL
        return size
class _BinaryPlist17Writer:
    def __init__(self, fp, sort_keys, skipkeys):
        self._fp = fp
        self._sort_keys = sort_keys
        self._skipkeys = skipkeys
    
    def write(self, value):
        plist_bytes = 'bplist17'.encode()
        current_position = len(plist_bytes)
        self._pack(value=value, position=current_position)

        self._fp.write(plist_bytes)

    def _pack(self, value, position):
        value_bytes : bytes = None
        if isinstance(value, dict):
            # TODO process dict
            print('process dict')
            endposition = position +  size
            header_bytes = b'\xD0' + endposition.to_bytes(length=8, byteorder='little')

        elif isinstance(value, (list, tuple)):
            # TODO process array
            print('process array')
            size = 1 # TODO get size of packed array contents
            endposition = position +  size
            header_bytes = b'\xA0' + endposition.to_bytes(length=8, byteorder='little')
        
        else:
            # TODO process scalars
            print('process scalars')

        return value_bytes
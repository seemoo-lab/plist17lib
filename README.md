# plist17lib
This python library allows to parse Apple's binary property list format in the version `bplist17` into a JSON representation and vice versa.
This is based on python's [plistlib](https://docs.python.org/3/library/plistlib.html) which does this for version `bplist00`.

Additionally, the JSON representation can contain type information.
We also provide command-line tools to convert between such binary and JSON files.

### List of possible types and their binary equivalent
The type information in the typed JSON representation corresponds to the type information in the binary format as follows:

(hexadecimal byte representaion in bplist binary - corresponding identifiers in json):
```
1X - "int",
22 - "float" (2^2 = 4 bytes), 
23 - "double" (2^3 = 8 bytes),
4X - "data.hexstring" (value was parsed as hexstring),
   - "data.bplist00" if data contains a bplist00 which was parsed as json,
   - "data.bplist17" if data contains a bplist17 which was parsed as json,
6X - "string_utf16le",
7X - "string_ascii",
A0 - "array",
B0/C0 - "bool" (value true/false),
D0 - "dict",
E0 - "null",
FX - "uint"
```
Type `8X` (address reference) does not have a corresponding type in the JSON format, since the objects are dereferenced by the parser.

The nibble `X` represents the length of the data if it has a value below 0xF. If it is 0xF, an integer containing the length follows (e.g. `11 20` for the length 0x20).
The length is specified in bytes, except for UTF16LE strings, where the length is specified as number of characters (aka half of the byte length). \
For arrays and dictionaries, the byte `A0` or `D0` is followed by the end address of the last byte of the array/dictionary (8 bytes, little-endian).

The unknown types `0X`, `5X` and `9X` (which may or may not exist) are not implemented by the parser, hence they have no no corresponding types in the json output.

# plist17lib

This module allows to parse bplist17 files into json files and vice versa.

These json files can contain type information.

### List of possible types 
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
AX - "array",
B0/C0 - "bool",
D0 - "dict",
E0 - "null",
FX - "uint"
```
Type 8X (address reference) does not have a corresponding type in the json format, since the objects are dereferenced by the parser.

The unknown types 0X, 5X, 9X (which may or may not exist) are not implemented by the parser, hence they have no no corresponding types in the json output.

# Define the parts of the 'six' package that we need.
# I don't want to introduce it as hard dependency.
import sys


PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

if PY3:
    string_types = (str,)
    # integer_types = (int,)
    text_type = str
    # binary_type = bytes
    # six has no char_types, but it should:
    # bytes + string + unicode, where defined.
    char_types = (bytes, str)
else:
    string_types = (basestring,)
    # integer_types = (int, long)
    text_type = unicode
    # binary_type = str
    char_types = string_types

import sys


VERSION = 3
if sys.version[0]=='2':
    VERSION = 2
    from UserDict import DictMixin
    import re
    # print("2")
elif sys.version[0]=='3':
    VERSION = 3
    from collections import UserDict
    import regex as re
    # print("3")


class ClobberedDictKey(Exception):
    "A flag that a variable has been assigned two incompatible values."
    pass

if VERSION==2:
    class NoClobberDict(DictMixin):

        """
        A dictionary-like object that prevents its values from being
        overwritten by different values. If that happens, it indicates a
        failure to match.
        """
        def __init__(self, initial_dict = None):
            if initial_dict == None:
                self._dict = {}
            else:
                self._dict = dict(initial_dict)
            
        def __getitem__(self, key):
            return self._dict[key]

        def __setitem__(self, key, value):
            # if self._dict.has_key(key) and self._dict[key] != value: #python2
            if key in self._dict and self._dict[key] != value:
                raise ClobberedDictKey((key, value))

            self._dict[key] = value

        def __delitem__(self, key):
            del self._dict[key]

        def __contains__(self, key):
            return self._dict.__contains__(key)

        def __iter__(self):
            return self._dict.__iter__()

        def iteritems(self):
            return self._dict.iteritems()
            
        def keys(self):
            return self._dict.keys()

elif VERSION==3:
    class NoClobberDict(UserDict): #for python3

        """
        A dictionary-like object that prevents its values from being
        overwritten by different values. If that happens, it indicates a
        failure to match.
        """
        def __init__(self, initial_dict = None):
            if initial_dict == None:
                self._dict = {}
            else:
                self._dict = dict(initial_dict)
            
        def __getitem__(self, key):
            return self._dict[key]

        def __setitem__(self, key, value):
            # if self._dict.has_key(key) and self._dict[key] != value: #python2
            if key in self._dict and self._dict[key] != value:
                raise ClobberedDictKey((key, value))

            self._dict[key] = value

        def __delitem__(self, key):
            del self._dict[key]

        def __contains__(self, key):
            return self._dict.__contains__(key)

        def __iter__(self):
            return self._dict.__iter__()

        def iteritems(self):
            return self._dict.iteritems()
            
        def keys(self):
            return self._dict.keys()


# A regular expression for finding variables.
AIRegex = re.compile(r'\(\?(\S+)\)')

def AIStringToRegex(AIStr):
    res =  AIRegex.sub( r'(?P<\1>[^ \t\n\r\f\v]+)', AIStr )+'$'
    return res


def AIStringToPyTemplate(AIStr):
    return AIRegex.sub( r'%(\1)s', AIStr )


def AIStringVars(AIStr):
    # This is not the fastest way of doing things, but
    # it is probably the most explicit and robust
    return set([ AIRegex.sub(r'\1', x) for x in AIRegex.findall(AIStr) ])
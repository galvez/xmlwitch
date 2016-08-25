from __future__ import with_statement
from xml.sax.saxutils import escape, quoteattr
from keyword import kwlist as PYTHON_KWORD_LIST
import sys

__all__ = ['Builder', 'Element']
__license__ = 'BSD'
__version__ = '0.3'
__author__ = "Jonas Galvez <http://jonasgalvez.com.br/>"
__contributors__ = ["bbolli <http://github.com/bbolli/>",
                    "masklinn <http://github.com/masklinn/>",
                    "kcsaff <http://github.com/kcsaff/>"]

#  Python 2 + 3 support

if sys.version_info[0] == 2:
    bytes = str
else:
    unicode = str

try:
    from io import BytesIO  # Python 3
except ImportError:
    try:
        from cStringIO import BytesIO  # Python 2, fast
    except ImportError:
        from StringIO import BytesIO  # Python 2, pure

# Code

class Builder:
    def __init__(self, encoding='utf-8', indent=' '*2, version=None, 
                 stream=None):
        self._document = stream or BytesIO()

        self._encoding = encoding
        self._indent = indent
        self._indentation = 0
        self._open_tag = None
        self._newline = ''
        self._to_str = self._to_bytes if str == bytes else self._to_unicode
        if version is not None:
            self.write('<?xml version="%s" encoding="%s"?>' % (
                version, encoding
            ))

    def __getattr__(self, name):
        return Element(name, self)

    def __getitem__(self, name):
        return Element(name, self)

    def _to_bytes(self, s):
        return s if isinstance(s, bytes) else s.encode(self._encoding)

    def _to_unicode(self, s):
        return s if isinstance(s, unicode) else s.decode(self._encoding)

    def __bytes__(self):
        return self._to_bytes(self.__getvalue())

    def __str__(self):
        return self._to_str(self.__getvalue())

    def __unicode__(self):
        return self._to_unicode(self.__getvalue())

    def __getvalue(self):
        self._open_tag and self._open_tag.close()
        if hasattr(self._document, 'getvalue'):
            return self._document.getvalue()
        else:
            return '<streaming %s object>' % self.__class__.__name__

    def __del__(self):
        self._open_tag and self._open_tag.close()

    def write(self, content):
        """Write raw content to the document"""
        self._document.write(self._to_bytes(content))
        self._newline = '\n'

    def write_escaped(self, content):
        """Write escaped content to the document"""
        self.write(escape(self._to_str(content)))

    def write_indented(self, content):
        """Write indented content to the document"""
        self.write('%s%s%s' % (self._newline, self._indent * self._indentation, self._to_str(content)))

builder = Builder  # 0.1 backward compatibility


class Element:
    PYTHON_KWORD_MAP = dict([(k + '_', k) for k in PYTHON_KWORD_LIST])

    def __init__(self, name, builder):
        self.name = self._nameprep(name)
        self.content = ''
        self.builder = builder
        self.builder._open_tag and self.builder._open_tag.close()
        self.builder.write_indented('<%s' % self.name)
        self.builder._open_tag = self

    def close(self):
        if self.builder._open_tag is self:
            if self.content:
                self.builder.write('>%s</%s>' % (self.content, self.name))
            else:
                self.builder.write(' />')
            self.builder._open_tag = None

    def __enter__(self):
        """Add a parent element to the document"""
        self.builder.write('>%s' % self.content)
        self.builder._indentation += 1
        self.builder._open_tag = None
        return self

    def __exit__(self, type, value, tb):
        """Add close tag to current parent element"""
        self.builder._open_tag and self.builder._open_tag.close()
        self.builder._indentation -= 1
        self.builder.write_indented('</%s>' % self.name)

    def __call__(*args, **kargs):
        """Add content & attributes to the opened tag"""
        self = args[0]
        for attr, value in sorted(kargs.items()):
            self.builder.write(' %s=%s' % (
                self._nameprep(attr), quoteattr(self.builder._to_str(value))
            ))
        for s in args[1:]:
            if s:
                self.content += escape(self.builder._to_str(s))
        return self

    def __del__(self):
        self.close()

    @classmethod
    def _nameprep(cls, name):
        """Undo keyword and colon mangling"""
        name = cls.PYTHON_KWORD_MAP.get(name, name)
        return name.replace('__', ':')

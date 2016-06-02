from __future__ import with_statement
from xml.sax import saxutils
from keyword import kwlist as PYTHON_KWORD_LIST
import sys

__all__ = ['Builder', 'Element']
__license__ = 'BSD'
__version__ = '0.2.1'
__author__ = "Jonas Galvez <http://jonasgalvez.com.br/>"
__contributors__ = ["bbolli <http://github.com/bbolli/>",
                    "masklinn <http://github.com/masklinn/>"]

class Builder:
    def __init__(self, encoding='utf-8', indent=' '*2, version=None, 
                 stream=None):
        self._document = stream if stream is not None else StringIO()

        self._encoding = encoding
        self._indent = indent
        self._indentation = 0
        self._open_element = None
        self._newline = ''
        if version is not None:
            self.write('<?xml version="%s" encoding="%s"?>' % (
                version, encoding
            ))

    def __getattr__(self, name):
        return Element(name, self)

    def __getitem__(self, name):
        return Element(name, self)

    def __str__(self):
        return to_str(self.__unicode__(), self._encoding)

    def __unicode__(self):
        if self._open_element:
            self._open_element.close()
        if hasattr(self._document, "getvalue"):
            return self._document.getvalue()
        else:
            return '<streaming %s object>' % self.__class__.__name__

    def __del__(self):
        if self._open_element:
            self._open_element.close()

    def write(self, content):
        """Write raw content to the document"""
        self._document.write(to_unicode(content, self._encoding))
        self._newline = '\n'

    def write_escaped(self, content):
        """Write escaped content to the document"""
        self.write(saxutils.escape(content))

    def write_indented(self, content):
        """Write indented content to the document"""
        self.write('%s%s%s' % (self._newline, self._indent * self._indentation, content))

builder = Builder # 0.1 backward compatibility

class Element:

    PYTHON_KWORD_MAP = dict([(k + '_', k) for k in PYTHON_KWORD_LIST])

    def __init__(self, name, builder):
        self.name = self._nameprep(name)
        self.builder = builder
        self.content = []
        if self.builder._open_element:
            self.builder._open_element.close()
        self.builder.write_indented('<%s' % self.name)
        self.builder._open_element = self

    def close(self):
        if self.content:
            self.builder.write('>%s</%s>' % (''.join(self.content), self.name))
        else:
            self.builder.write(' />')
        self.builder._open_element = None

    def __enter__(self):
        """Add a parent element to the document"""
        self.builder.write('>%s' % ''.join(self.content))
        self.builder._indentation += 1
        self.builder._open_element = None
        return self

    def __exit__(self, type, value, tb):
        """Add close tag to current parent element"""
        self.builder._indentation -= 1
        if self.builder._open_element:
            self.builder._open_element.close()
        self.builder.write_indented('</%s>' % self.name)

    def __call__(*args, **kargs):
        """Add a child element to the document"""
        self = args[0]
        for attr, value in kargs.items():
            self.builder.write(' %s=%s' % (
                self._nameprep(attr), saxutils.quoteattr(value)
            ))
        self.content.extend([saxutils.escape(s) for s in args[1:] if s])
        return self

    def __del__(self):
        if self.builder._open_element is self:
            self.close()

    @classmethod
    def _nameprep(cls, name):
        """Undo keyword and colon mangling"""
        name = Element.PYTHON_KWORD_MAP.get(name, name)
        return name.replace('__', ':')

#  Python 2 + 3 support

if sys.version_info[0] == 2:
    def to_str(u, encoding):
        return u if isinstance(u, str) else u.encode(encoding)

    def to_unicode(s, encoding):
        return s if isinstance(s, unicode) else s.decode(encoding)
else:  # Python 3, unicode == str
    def to_str(u, _):
        return u

    to_unicode = to_str

try:
    from io import StringIO  # Python 3
except ImportError:
    try:
        from cStringIO import StringIO  # Python 2, fast
    except ImportError:
        from StringIO import StringIO  # Python 2, pure

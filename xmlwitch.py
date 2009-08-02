from __future__ import with_statement
from StringIO import StringIO
from xml.sax import saxutils
from keyword import kwlist as PYTHON_KWORD_LIST

__all__ = ['__author__', '__license__', 'builder', 'element']
__license__ = 'GPL'
__author__ = ('Jonas Galvez', 'jonas@codeazur.com.br', 'http://jonasgalvez.com.br')
__contributors__ = [('Beat Bolli', 'http://drbeat.li/'), # bbolli, maskliin, change this as you like
                    ('masklinn', 'http://github.com/masklinn')]

class builder:
  def __init__(self, version, encoding):
    self._document = StringIO()
    self._document.write('<?xml version="%s" encoding="%s"?>\n' % (version, encoding))
    self._encoding = encoding
    self._unicode = (encoding == 'utf-8')
    self._indentation = 0
    self._indent = '  '
  def __getattr__(self, name):
    return element(name, self)
  __getitem__ = __getattr__
  def __str__(self):
    return self._document.getvalue().encode(self._encoding)
  def __unicode__(self):
    return self._document.getvalue().decode(self._encoding)
  def _write(self, line):
    line = line.decode(self._encoding)
    self._document.write('%s%s\n' % (self._indentation * self._indent, line))

class element:
  _dummy = {}
  PYTHON_KWORD_MAP = dict([(k + '_', k) for k in PYTHON_KWORD_LIST])
  def __init__(self, name, builder):
    self.name = self.nameprep(name)
    self.builder = builder
    self.attributes = {}
  def __enter__(self):
    self.builder._write('<%s%s>' % (self.name, self.serialized_attrs))
    self.builder._indentation += 1
    return self
  def __exit__(self, type, value, tb):
    self.builder._indentation -= 1
    self.builder._write('</%s>' % self.name)
  def __call__(self, _value=_dummy, **kargs):
    self.attributes.update(kargs)
    if _value is None:
      self.builder._write('<%s%s />' % (self.name, self.serialized_attrs))
    elif _value != element._dummy:
      self.builder._write('<%s%s>%s</%s>' % (self.name, self.serialized_attrs, saxutils.escape(_value), self.name))
      return
    return self
  @property
  def serialized_attrs(self):
    serialized = []
    for attr, value in self.attributes.items():
      serialized.append(' %s=%s' % (self.nameprep(attr), saxutils.quoteattr(value)))
    return ''.join(serialized)
  def nameprep(self, name):
    """Undo keyword and colon mangling"""
    name = element.PYTHON_KWORD_MAP.get(name, name)
    return name.replace('__', ':')
  def text(self, value):
    self.builder._write(saxutils.escape(value))

if __name__ == "__main__":
  xml = builder(version="1.0", encoding="utf-8")
  with xml.feed(xmlns='http://www.w3.org/2005/Atom'):
    xml.title('Example Feed')
    xml.link(None, href='http://example.org/')
    xml.updated('2003-12-13T18:30:02Z')
    with xml.author:
      xml.name('John Doe')
    xml.id('urn:uuid:60a76c80-d399-11d9-b93C-0003939e0af6')
    with xml.entry:
      xml['my:elem']("Hello these are namespaces!", **{'xmlns:my':'http://example.org/ns/', 'my:attr':'what?'})
      xml.my__elem("Hello these are namespaces!", xmlns__my='http://example.org/ns/', my__attr='what?')
      xml.quoting("< > & ' \"", attr="< > & ' \"")
      xml.title('Atom-Powered Robots Run Amok')
      xml.link(None, href='http://example.org/2003/12/13/atom03')
      xml.id('urn:uuid:1225c695-cfb8-4ebb-aaaa-80da344efa6a')
      xml.updated('2003-12-13T18:30:02Z')
      xml.summary('Some text.')
      with xml.content(type='xhtml'):
        with xml.div(xmlns='http://www.w3.org/1999/xhtml') as div:
          xml.label('Some label', for_='some_field')
          div.text(':')
          xml.input(None, type='text', value='')
  print xml

from __future__ import with_statement
from StringIO import StringIO
from exceptions import UnicodeDecodeError

__all__ = ['__author__', '__license__', 'builder', 'element']
__author__ = ('Jonas Galvez', 'jonas@codeazur.com.br', 'http://jonasgalvez.com.br')
__license__ = "GPL"


class builder:
  def __init__(self, version, encoding):
    self.document = StringIO()
    self.document.write('<?xml version="%s" encoding="%s"?>\n' % (version, encoding))
    self.unicode = (encoding == 'utf-8')
    self.indentation = 0
    self.indent = '  '
  def __getattr__(self, name):
    return element(name, self)
  __getitem__ = __getattr__
  def __str__(self):
    if self.unicode:
      return self.document.getvalue().encode('utf-8')
    return self.document.getvalue()
  def __unicode__(self):
    return self.document.getvalue().decode('utf-8')
  def write(self, line):
    if self.unicode:
      line = line.decode('utf-8')
    self.document.write('%s%s' % ((self.indentation * self.indent), line))

_dummy = {}

class element:
  def __init__(self, name, builder):
    self.name = name
    self.builder = builder
    self.serialized_attrs = ''
  def __enter__(self):
    self.builder.write('<%s%s>\n' % (self.name, self.serialized_attrs))
    self.builder.indentation += 1
  def __exit__(self, type, value, tb):
    self.builder.indentation -= 1
    self.builder.write('</%s>\n' % self.name)
  def __call__(self, value=_dummy, **kargs):
    if kargs:
      self.serialized_attrs = self.serialize_attrs(kargs)
    if value == None:
      self.builder.write('<%s%s />\n' % (self.name, self.serialized_attrs))
    elif value != _dummy:
      self.builder.write('<%s%s>%s</%s>\n' % (self.name, self.serialized_attrs, value, self.name))
      return
    return self
  def serialize_attrs(self, attrs):
    serialized = []
    for attr, value in attrs.items():
      serialized.append(' %s="%s"' % (attr, value))
    return ''.join(serialized)

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
      xml["my:namespace"]("Hello these are namespaces!")
      xml.title('Atom-Powered Robots Run Amok')
      xml.link(None, href='http://example.org/2003/12/13/atom03')
      xml.id('urn:uuid:1225c695-cfb8-4ebb-aaaa-80da344efa6a')
      xml.updated('2003-12-13T18:30:02Z')
      xml.summary('Some text.')
  print xml

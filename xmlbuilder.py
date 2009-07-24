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
    self.indentation = -2
  def __getattr__(self, name):
    return element(name, self)
  def __getitem__(self, name):
    return element(name, self)
  def __str__(self):
    if self.unicode:
      return self.document.getvalue().encode('utf-8')
    return self.document.getvalue()
  def __unicode__(self):
    return self.document.getvalue().decode('utf-8')
  def write(self, line):
    if self.unicode:
      line = line.decode('utf-8')
    self.document.write('%s%s' % ((self.indentation * ' '), line))

_dummy = {}

class element:
  def __init__(self, name, builder):
    self.name = name
    self.builder = builder
  def __enter__(self):
    self.builder.indentation += 2
    if hasattr(self, 'attributes'):
      self.builder.write('<%s %s>\n' % (self.name, self.serialized_attrs))
    else:
      self.builder.write('<%s>\n' % self.name)
  def __exit__(self, type, value, tb):
    self.builder.write('</%s>\n' % self.name)
    self.builder.indentation -= 2
  def __call__(self, value=_dummy, **kargs):
    if len(kargs.keys()) > 0:
      self.attributes = kargs
      self.serialized_attrs = self.serialize_attrs(kargs)
    if value == None:
      self.builder.indentation += 2
      if hasattr(self, 'attributes'):
        self.builder.write('<%s %s />\n' % (self.name, self.serialized_attrs))
      else:
        self.builder.write('<%s />\n' % self.name)
      self.builder.indentation -= 2
    elif value != _dummy:
      self.builder.indentation += 2
      if hasattr(self, 'attributes'):
        self.builder.write('<%s %s>%s</%s>\n' % (self.name, self.serialized_attrs, value, self.name))
      else:
        self.builder.write('<%s>%s</%s>\n' % (self.name, value, self.name))
      self.builder.indentation -= 2
      return
    return self
  def serialize_attrs(self, attrs):
    serialized = []
    for attr, value in attrs.items():
      serialized.append('%s="%s"' % (attr, value))
    return ' '.join(serialized)

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

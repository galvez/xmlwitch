from __future__ import with_statement
from exceptions import UnicodeDecodeError

from StringIO import StringIO
try:
  from cStringIO import StringIO
except ImportError: pass

from xml.etree.ElementTree import ElementTree, Element, QName, tostring
try:
  from xml.etree.cElementTree import ElementTree, Element, QName, tostring
except ImportError: pass

__all__ = ['__author__', '__license__', 'builder', 'element']
__author__ = ('Jonas Galvez', 'jonas@codeazur.com.br', 'http://jonasgalvez.com.br')
__license__ = "GPL"

# Because the elementtree included in Python doesn't have a pretty printer
def indent(elem, indentation=2, level=0):
    i = "\n" + level*indentation*" "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + indentation*" "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, indentation, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

def normalize(name):
  """ Normalize a builder qname to ensure that it can be used by ElementTree:
  * If it's a tuple, build a QName object from it
  * Otherwise, pass it through (ET will handle names and clark's notation names)
  """
  if type(name) == tuple:
    return QName(*name)
  return name

class builder:
  def __init__(self, encoding='utf-8', version='1.0'):
    self._tree = None
    self._context = []
    self._encoding = encoding

  def __getattr__(self, name):
    return element(name, self)
  def __getitem__(self, name):
    return element(name, self)

  def tostring(self, indentation=2):
    output = StringIO()
    indent(self._tree.getroot(), indentation)
    self._tree.write(output, self._encoding)
    return output.getvalue()
  def __str__(self):
    return self.tostring()
  def __unicode__(self):
    return str(self).decode(self._encoding)

  def _send(self, element):
    """ Receive a new element to add to the current context

    Add the element as subelement of the context tip.
    If there is no context, there should be no tree. Create the tree
    and add element as its root.

    If there's an empty context but there's a tree, it means we're writing
    out of the tree root, which is an error.
    """
    if not self._context:
      assert not self._tree
      self._tree = ElementTree(element._node)
    else:
      self._context[-1].append(element._node)
  def _push(self, element):
    """ Push an `element` instance on the context stack

    this element will be used as reference for new elements until it's popped
    """
    self._context.append(element._node)
  def _pop(self, element):
    assert element._node is self._context[-1]
    self._context.pop()

class element:
  def __init__(self, name, builder):
    self._node = Element(normalize(name))

    self.builder = builder
    self.builder._send(self)

  def __enter__(self):
    self.builder._push(self)
    return self
  def __exit__(self, type, value, tb):
    self.builder._pop(self)

  def __call__(self, value=None, **kwargs):
    self._node.attrib.update(kwargs)
    self._node.text = value

    return self

  def __setitem__(self, attribute, value):
    self._node.set(normalize(attribute), value)
  def __getitem__(self, attribute):
    return self._node.get(normalize(attribute))

  def __repr__(self):
    return repr(self._node)

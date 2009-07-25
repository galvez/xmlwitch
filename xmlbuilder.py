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
def indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

class builder:
  def __init__(self, encoding='utf-8', version='1.0'):
    self._tree = None
    self._context = []
    self._encoding = encoding

  def __getattr__(self, name):
    return element(name, self)
  def __getitem__(self, name):
    return element(name, self)

  def __str__(self):
    output = StringIO()
    indent(self._tree.getroot())
    self._tree.write(output, self._encoding)
    return output.getvalue()
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

_dummy = {}

class element:
  def __init__(self, name, builder):
    if type(name) == tuple:
      self._node = Element(QName(*name))
    else:
      self._node = Element(name)
    self.builder = builder
    self.builder._send(self)

  def __enter__(self):
    self.builder._push(self)
  def __exit__(self, type, value, tb):
    self.builder._pop(self)

  def __call__(self, value=None, **kwargs):
    self._node.attrib.update(kwargs)
    self._node.text = value

    return self

  def __repr__(self):
    return repr(self._node)

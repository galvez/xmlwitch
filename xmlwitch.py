# -*- coding: utf-8; c-basic-offset: 2; indent-tabs-mode: nil -*-

from __future__ import with_statement
from exceptions import UnicodeDecodeError
from keyword import kwlist

try:
  from cStringIO import StringIO
except ImportError:
  from StringIO import StringIO

try:
  from xml.etree.cElementTree import ElementTree, Element, QName, tostring
except ImportError:
  from xml.etree.ElementTree import ElementTree, Element, QName, tostring

__all__ = ['__author__', '__license__', 'builder', 'element']
__license__ = 'BSD'
__author__ = ('Jonas Galvez', 'jonas@codeazur.com.br', 'http://jonasgalvez.com.br')
__contributors__ = [('Beat Bolli', 'http://drbeat.li/'),
                    ('masklinn', 'http://github.com/masklinn')]

# Because the elementtree included in Python doesn't have a pretty printer
def _indent(elem, indentation=2, level=0):
  i = "\n" + level*indentation*" "
  if len(elem):
    if not elem.text or not elem.text.strip():
      elem.text = i + indentation*" "
    if not elem.tail or not elem.tail.strip():
      elem.tail = i
    for elem in elem:
      _indent(elem, indentation, level+1)
    if not elem.tail or not elem.tail.strip():
      elem.tail = i
  else:
    if level and (not elem.tail or not elem.tail.strip()):
      elem.tail = i

def _normalize(name):
  """ Normalize a builder qname to ensure that it can be used by ElementTree:
  * If it's a tuple, build a QName object from it
  * Otherwise, pass it through (ET will handle names and clark's notation names)
  """
  if type(name) == tuple:
    return QName(*name)
  return name

KEYWORD_UNMANGLER = dict((k + '_', k) for k in kwlist)
def _unmangle_attribute_name(key):
  """ To use Python keywords as attribute names, they can be postfixed with an
  underscore. Undo that to store the correct attribute name
  """
  if key in KEYWORD_UNMANGLER:
    return KEYWORD_UNMANGLER[key]
  return key

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
    _indent(self._tree.getroot(), indentation)
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
    self._node = Element(_normalize(name))

    self.builder = builder
    self.builder._send(self)

  def __enter__(self):
    self.builder._push(self)
    return self
  def __exit__(self, type, value, tb):
    self.builder._pop(self)

  def __call__(self, _text=None, **kwargs):
    kwargs = dict((_unmangle_attribute_name(key), value)
                  for key, value in kwargs.iteritems())
    self._node.attrib.update(kwargs)
    self.text(_text)

    return self

  def text(self, value):
    """ Append a text node to the element
    """
    # if no children, append value to text
    if not len(self._node):
      if self._node.text:
        self._node.text += value
      else:
        self._node.text = value
    else:
      # otherwise ET sucks at text, append value to tail
      # of last child...
      last_child = self._node[-1]
      if last_child.tail: last_child.tail += value
      else: last_child.tail = value
    return self

  def __setitem__(self, attribute, value):
    self._node.set(_normalize(attribute), value)
  def __getitem__(self, attribute):
    return self._node.get(_normalize(attribute))

  def __repr__(self):
    return repr(self._node)

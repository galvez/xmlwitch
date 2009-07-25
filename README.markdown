# CHANGES:

* Uses xml.etree.ElementTree rather than text mangling
* Encoding and version are now optional (defaulting to utf-8 and 1.0)
* Unless the encoding is altered, the XML prefix won't be included (it's optional anyway)
* Namespace handling reworked, use Clark's notation or (namespace, element) to specify them
* Added `builder.tostring` method for custom indentation of the output tree (default = 2 spaces per indentation level)
* Added some doctests

# TODO:

* Handle default namespace (elementtree 1.2 has no concept for it, how?), beware of the dichotomy between attributes and elements on that.

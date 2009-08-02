# xmlwitch

[xmlwitch](http://pypi.python.org/pypi/xmlwitch/) is a reimplementation of [Ruby's Builder](http://builder.rubyforge.org/) library written and mantained by [Jonas Galvez](http://jonasgalvez.com.br/). It uses a very different technique (Python's context processors) but delivers an extremely similar syntax. xmlwitch leverages the with statement which makes it dependent on Python 2.5 and above.

Since the number of patches and other contributions have been greater than what I expected, I've created a mailing-list to help coordinate further improvements (if at all necessary): [http://groups.google.com/group/xmlwitch-dev](http://groups.google.com/group/xmlwitch-dev/).

## history

* **TODO: go over galvez/master and update this section with dates and proper credits**
 
## the says-it-all usage example

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
    print xml # str(xml)
  
## contributing guidelines

- 2-space identation, please (or I'll shoot you!)
- no global functions, keep things logically namespaced
- avoid list comprehensions that can't be written in a single line (e.g., 79 columns)
- no clever tricks or deep monkey patching of python's standard library 

## contributors

- [Beat Bolli](http://github.com/bbolli/)
- [masklinn](http://github.com/masklinn/)
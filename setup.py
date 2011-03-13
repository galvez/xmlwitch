"""
xmlwitch offers Pythonic XML generation through context generators in a 
minimalist implementation with less than 100 lines of code. BSD-licensed.

Usage
`````

::

    import xmlwitch
    xml = xmlwitch.Builder(version='1.0', encoding='utf-8')
    with xml.feed(xmlns='http://www.w3.org/2005/Atom'):
        xml.title('Example Feed')
        xml.updated('2003-12-13T18:30:02Z')
        with xml.author:
            xml.name('John Doe')
        xml.id('urn:uuid:60a76c80-d399-11d9-b93C-0003939e0af6')
        with xml.entry:
            xml.title('Atom-Powered Robots Run Amok')
            xml.id('urn:uuid:1225c695-cfb8-4ebb-aaaa-80da344efa6a')
            xml.updated('2003-12-13T18:30:02Z')
            xml.summary('Some text.')
    print(xml)

Setup
`````

::

    $ pip install xmlwitch # or
    $ easy_install xmlwitch # or
    $ cd xmlwitch-0.2; python setup.py install

Links
`````

* `Full documentation <http://jonasgalvez.com.br/Software/XMLWitch.html>`_
* `Development repository <http://github.com/galvez/xmlwitch/>`_
* `Author's website <http://jonasgalvez.com.br/>`_

"""

from distutils.core import setup

setup(
    name = 'xmlwitch',
    version = '0.2.1',
    url = 'http://jonasgalvez.com.br/Software/XMLWitch.html',
    license = 'BSD',
    author = "Jonas Galvez",
    author_email = "jonasgalvez@gmail.com",
    description = "xmlwitch offers Pythonic XML generation through context generators",
    long_description = __doc__,
    py_modules = ['xmlwitch'],
    platforms = 'Python 2.5 and later',
    classifiers = [
        'Intended Audience :: Developers',
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries',
        'Topic :: Text Processing :: Markup :: HTML',
        'Topic :: Text Processing :: Markup :: XML'
    ]
)
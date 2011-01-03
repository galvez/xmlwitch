**xmlwitch** is a BSD-licensed, Python 2.5+ library that offers idiomatic XML generation through context managers (with statement) in a minimalist implementation with less than 100 lines of code. To install, just run **pip install xmlwitch**, **easy_install xmlwitch** or copy **xmlwitch.py** to your appropriate project's directory. It's just one file.

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

Please refer to [http://jonasgalvez.com.br/Software/XMLWitch.html](http://jonasgalvez.com.br/Software/XMLWitch.html) for further info.

Thanks to [maskllin](http://github.com/masklinn/) and [bbolli](http://github.com/bbolli/) for contributions. Pull requests are welcome.
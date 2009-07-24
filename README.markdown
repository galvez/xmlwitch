    from xmlbuilder import builder

    xml = builder(version="1.0", encoding="utf-8")
    with xml.feed(xmlns='http://www.w3.org/2005/Atom'):
      xml['title']('Example Feed')
      xml.link(None, href='http://example.org/')
      xml.updated('2003-12-13T18:30:02Z')
      with xml.author:
        xml.name('John Doe')
      xml.id('urn:uuid:60a76c80-d399-11d9-b93C-0003939e0af6')
      with xml.entry:
        xml.title('Atom-Powered Robots Run Amok')
        xml.link(None, href='http://example.org/2003/12/13/atom03')
        xml.id('urn:uuid:1225c695-cfb8-4ebb-aaaa-80da344efa6a')
        xml.updated('2003-12-13T18:30:02Z')
        xml.summary('Some text.')
    print xml
from __future__ import with_statement

import sys
import os

ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__), '..'
    )
)
sys.path.append(ROOT)

import unittest
import xmlwitch

class XMLWitchTestCase(unittest.TestCase):
    
    def expected_document(self, filename):
        expected = os.path.join(ROOT, 'tests',  'expected',  filename)
        with open(expected) as document:
            return document.read()
            
    def test_simple_document(self):
            xml = xmlwitch.Builder(version='1.0', encoding='utf-8')
            with xml.person:
                xml.name("Bob")
                xml.city("Qusqu")
            self.assertEquals(
                str(xml), 
                self.expected_document('simple_document.xml')
            )
    
    def test_utf8_document(self):
        string = u"""An animated fantasy film from 1978 based on the first """ \
                 u"""half of J.R.R Tolkien\u2019s Lord of the Rings novel. The """ \
                 u"""film was mainly filmed using rotoscoping, meaning it was """ \
                 u"""filmed in live action sequences with real actors and then """ \
                 u"""each frame was individually animated."""
        xml = xmlwitch.Builder(version='1.0', encoding='utf-8')
        with xml.test:
             xml.description(string)
        
        self.assertEquals(
            str(xml),
            self.expected_document('utf8_document.xml')
        )
    
    def test_nested_elements(self):
        xml = xmlwitch.Builder()
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
        self.assertEquals(
            str(xml), 
            self.expected_document('nested_elements.xml')
        )
    
    def test_rootless_fragment(self):
        xml = xmlwitch.Builder()
        xml.data(None, value='Just some data')
        self.assertEquals(
            str(xml), 
            self.expected_document('rootless_fragment.xml')
        )
    
    def test_content_escaping(self):
        xml = xmlwitch.Builder()
        with xml.doc:
            xml.item('Text&to<escape', some_attr='attribute&value>to<escape')
        self.assertEquals(
            str(xml), 
            self.expected_document('content_escaping.xml')
        )
    
    def test_namespaces(self):
        xml = xmlwitch.Builder()
        with xml.parent(**{'xmlns:my':'http://example.org/ns/'}):
            xml.my__child(None, my__attr='foo')
        self.assertEquals(
            str(xml), 
            self.expected_document('namespaces.xml')
        )        
    
    def test_atom_feed(self):
        xml = xmlwitch.Builder(version="1.0", encoding="utf-8")
        with xml.feed(xmlns='http://www.w3.org/2005/Atom'):
            xml.title('Example Feed')
            xml.link(None, href='http://example.org/')
            xml.updated('2003-12-13T18:30:02Z')
            with xml.author:
                xml.name('John Doe')
                xml.id('urn:uuid:60a76c80-d399-11d9-b93C-0003939e0af6')
                xml.title('Atom-Powered Robots Run Amok')
                xml.link(None, href='http://example.org/2003/12/13/atom03')
                xml.id('urn:uuid:1225c695-cfb8-4ebb-aaaa-80da344efa6a')
                xml.updated('2003-12-13T18:30:02Z')
                xml.summary('Some text.')
                with xml.content(type='xhtml'):
                    with xml.div(xmlns='http://www.w3.org/1999/xhtml'):
                        xml.label('Some label', for_='some_field')
                        xml.input(None, type='text', value='')
        self.assertEquals(
            str(xml), 
            self.expected_document('atom_feed.xml')
        )

if __name__ == '__main__':
    unittest.main()
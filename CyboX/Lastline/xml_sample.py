'''
Created on 2015/03/11

@author: Makoto
'''
from xml.etree.ElementTree import *
from xml.sax.handler import ContentHandler
import xml.sax
import sys

fpath = "cfe629ab66a4446588a03a8c5aaede7b.xml"

class countHundler(ContentHandler):
    def __init__(self):
        self.tags={}
    def startElement(self, name, attrs):
        self.tags[name] = 1 + self.tags.get(name,0)

class textHundler(ContentHandler):
    def characters(self, ch):
        sys.stdout.write(ch.encode("Latin-1"))

def counttag():
    parser = xml.sax.make_parser()
    handler = countHundler()
    parser.setContentHandler(handler)
    parser.parse(fpath)
    tags = handler.tags.keys()
    tags.sort()
    for tag in tags:
        print tag, handler.tags[tag]

def textExtract():
    parser = xml.sax.make_parser()
    handler = textHundler()
    parser.setContentHandler(handler)
    texts = parser.parse(fpath)
    #print texts
    
def iterparent(elem):
    for parent in elem.getiterator():
        for child in parent:
            yield parent, child

def last_xml():
    tree = parse(fpath)
    root = tree.getroot()
    ss =  root.get("data")
    analysis =  root.findall(".//registry_reads")   
    for e in analysis:
        print e.tag, e.attrib
    #for p,c in iterparent(root):
    #    print c.tag+":"+p.tag

    
if __name__ == '__main__':
    
    last_xml()
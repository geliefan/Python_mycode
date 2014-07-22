# -*- coding: utf-8 -*-
import sys
import codecs
import MeCab

def ExtractNorn(text):
    tagger = MeCab.Tagger(r'-u C:\Software\MeCab\dic\naistdic\user.dic')
    node = tagger.parseToNode(text.encode('utf-8'))
    keywords = []
    i=10
    while node:
        item = node.feature.split(",")
        if item[0] == r"名詞" or item[0] == r"動詞":
            if i>0:  print node.surface
            i -= 1
            keywords.append(node.surface.decode('utf-8'))
        node = node.next
    return keywords

text = open("Protection_of_Personal_Information_utf8.txt","r").read()
nodes = ExtractNorn(text)
#tagger = MeCab.Tagger(r'-u C:\Software\MeCab\dic\naistdic\user.dic')
#node = tagger.parse(text)
txt = open("split.txt","w")
txt.write(str(nodes))

"""
for item in nodes:
    txt.write(item)
"""

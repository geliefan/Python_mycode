#config:utf-8
import sys
import codecs
import MeCab

def ExtractNorn(text):
    tagger = MeCab.Tagger(r'-u C:\Software\MeCab\dic\naistdic\user.dic')
    node = tagger.parseToNode(text)
    keywords = []
    while node:
        keywords.append(node.surface.decode('utf-8'))
        node = node.next
    return keywords

text = open("Protection_of_Personal_Information.txt","r").read()
#nodes = ExtractNorn(text)
tagger = MeCab.Tagger(r'-u C:\Software\MeCab\dic\naistdic\user.dic')
node = tagger.parse(text)
txt = open("mecab.txt","w")
txt.write(node)

"""
for item in nodes:
    txt.write(item)
"""

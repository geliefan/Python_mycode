# -*- coding: utf-8 -*-
import sys
import codecs
import MeCab

def ExtractNorn(text):
    tagger = MeCab.Tagger(r'-u C:\Software\MeCab\dic\naistdic\user.dic')
    encodes = text.encode("utf-8")
    node = tagger.parseToNode(encodes)
    keywords = []
    while node:
        """
        item = node.feature.split(",")
        if item[0] == r"名詞" or item[0] == r"動詞":
            if i>0:  print node.surface
            i -= 1
            keywords.append(node.surface.decode('utf-8'))
        """
        # 索引語だけ取り出す
        decode_node = node.surface.decode('utf-8')
        node_class = node.feature.split(",")[0]
        if  node_class == r"名詞":
            keywords.append(decode_node)
        elif node_class == r"動詞":
            keywords.append(decode_node)
        elif decode_node == r'。':
            keywords.append(decode_node)
        node = node.next
    return keywords

text = codecs.open("Protection_of_Personal_Information_utf8.txt","r",'utf-8').read()
nodes = ExtractNorn(text)
#tagger = MeCab.Tagger(r'-u C:\Software\MeCab\dic\naistdic\user.dic')
#node = tagger.parse(text)
txt = codecs.open("split.txt","w","utf-8")
for item in nodes:
  txt.write(item)
  if item == r'。':
    txt.write('\n')

"""
for item in nodes:
    txt.write(item)
"""

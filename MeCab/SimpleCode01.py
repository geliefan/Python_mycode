#coding:utf-8
import sys
import codecs
import MeCab

tagger=MeCab.Tagger("-Ochasen")
text=codecs.open('case01.txt','r','utf-8').read()
encode_text = text.encode('utf-8')
node=tagger.parse(encode_text)
result = node.decode('utf-8')

for item in result:
    print item[0],
"""
while result:
    item = result[0]
    print item,
    if result.next: break
"""

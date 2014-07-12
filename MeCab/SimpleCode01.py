#coding:utf-8
import sys
import codecs
import MeCab

<<<<<<< HEAD
tagger=MeCab.Tagger("-u user.dic")
=======
tagger=MeCab.Tagger("-Ochasen")
>>>>>>> 94a6e2a0f2448fa2bd9cb3c431b0d604e56c410c
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

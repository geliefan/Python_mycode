#coding:utf-8
import sys
import codecs
import MeCab

<<<<<<< HEAD
def extractKeyword(text):
    """textを形態素解析して、名詞のみのリストを返す"""
    tagger=MeCab.Tagger('-u C:\pg\MeCab\dic\ipadic\user.dic')
    node = tagger.parseToNode(text.encode('utf-8'))
    keywords = []
    while node:
        keywords.append(node.surface.decode("utf-8"))
        node = node.next
    return keywords
=======
<<<<<<< HEAD
tagger=MeCab.Tagger("-u user.dic")
=======
tagger=MeCab.Tagger("-Ochasen")
>>>>>>> 94a6e2a0f2448fa2bd9cb3c431b0d604e56c410c
text=codecs.open('case01.txt','r','utf-8').read()
encode_text = text.encode('utf-8')
node=tagger.parse(encode_text)
result = node.decode('utf-8')
>>>>>>> 2e9e213bff965730bd22357baa49f9b06cb73df2

text=codecs.open('case02.txt','r','utf-8').read()
nodes= extractKeyword(text)

for item in nodes:
    print item+"_",
"""
while result:
    item = result[0]
    print item,
    if result.next: break
"""



#coding:utf-8
import sys
import codecs
import MeCab

def extractKeyword(text):
    """textを形態素解析して、名詞のみのリストを返す"""
    tagger=MeCab.Tagger('-u C:\pg\MeCab\dic\ipadic\user.dic')
    node = tagger.parseToNode(text.encode('utf-8'))
    keywords = []
    while node:
        keywords.append(node.surface.decode("utf-8"))
        node = node.next
    return keywords

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



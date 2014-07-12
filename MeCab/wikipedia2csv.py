#coding:utf-8
import codecs
import re
import unicodedata
import sys

# wikipedia2csv.py

alias = re.compile(ur"_\(.*?\)")
alldigit = re.compile(ur"^[0-9]+$")

def isValid(word):
    """wordが登録対象の単語のときTrueを返す"""
    # 1文字の単語は登録しない
    if len(word) == 1:
        return False
    # コジコジ_(小惑星)のように別名は登録しない
    if alias.search(word) != None:
        return False
    # 数字だけの単語は登録しない
    if alldigit.search(word) != None:
        return False
    # 仮名2文字の単語は登録しない
    if len(word) == 2 and unicodedata.name(word[0])[0:8] == "HIRAGANA" and unicodedata.name(word[1])[0:8] == "HIRAGANA":
        return False
    # 仮名、漢字、数字、英字以外の文字を含む単語は登録しない
    for c in word:
        if not (unicodedata.name(c)[0:8] == "HIRAGANA" or
                unicodedata.name(c)[0:8] == "KATAKANA" or
                unicodedata.name(c)[0:3] == "CJK" or
                unicodedata.name(c)[0:5] == "DIGIT" or
                unicodedata.name(c)[0:5] == "LATIN"):
            return False
    return True

if __name__ == "__main__":
    fout = codecs.open("user.csv", "w", "utf-8")
    fin = codecs.open("jawiki-latest-all-titles-in-ns0", "r", "utf-8")
    for line in fin:
        word = line.rstrip()
        # Wikipedia見出し語を整形
        if isValid(word):
            cost = int(max(-36000, -400 * len(word)**1.5))
            fout.write("%s,-1,-1,%d,名詞,一般,*,*,*,*,*,*,*,wikipedia\n" % (word, cost))
    fin.close()
    fout.close()

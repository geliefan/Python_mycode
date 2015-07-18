# -*- coding:utf-8
'''
Created on 2015/03/18
pythonクックブック　4.16
メソッドや関数の発行にディクショナリを使う
@author: Makoto
'''

animals = []
number_of_felines = 0
def deal_with_a_cat():
    global number_of_felines
    print "meow"
    animals.append('feline')
    number_of_felines += 1
def deal_with_a_dog():
    print 'bark'
    animals.append('canine')
def deal_with_a_bear():
    print "watch out for the *HUG*!"
    animals.append('ursine')
tokenDict = {
             "cat": deal_with_a_cat,
             "dog": deal_with_a_dog,
             "bear": deal_with_a_bear
            }
# ファイルか何かから単語入力をシミュレート
words = ["cat","bear","cat","dog"]
for word in words:
    # wordに対してコールすべき関数を探してコール
    tokenDict[word]()
nf = number_of_felines
print 'we met %d feline%s' % (nf, 's'[nf==1:])
print 'the animals we met were:',' '.join(animals)
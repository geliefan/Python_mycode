# -*- coding:utf-8 -*-
'''
UnicodeDecodeErrorがとにかく出るからその対象方法を学習するためのモジュール
参考サイト
http://lab.hde.co.jp/2008/08/pythonunicodeencodeerror.html

'''
import sys
u1 = u'これは'
print type(u1)
print type(u1.encode('utf-8'))
print u1.encode('utf_8')
s1 = 'これは普通の文字列です'
print type(s1)
print s1 == u1.encode('utf-8')
print sys.getdefaultencoding()

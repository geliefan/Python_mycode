# -*- coding=utf-8 -*-
'''
Created on 2015/01/17

@author: Makoto
CSV Line Errorが生じたので，NULLが含まれていないかチェック
'''

import codecs
import csv

def checks(filepath):
    print repr(open(filepath, 'rb').read(200)) # dump 1st 200 bytes of file
    data = open(filepath, 'rb').read()
    print data.find('\xfea')
    print data.count('\xfea')

def fixCVS(filepath):
    fi = open(filepath, 'rb')
    data = fi.read()
    fi.close()
    fo = open('fixedCVS_ver02.log', 'wb')
    fo.write(data.replace('\x00', ''))
    fo.close()
    
if __name__ == '__main__':
    filepath = r'sample.log'
    #checks(filepath)
    #fixCVS(filepath)
    f = open('sample.log', 'rb').read()
    bom= codecs.BOM_UTF16_LE
    assert(f[:len(bom)]==bom)
    print f[len(bom):].decode('utf-16le')
    
# -*- coding=utf-8 -*-
'''
Created on 2015/01/17

@author: Makoto
CSV Line Errorが生じたので，NULLが含まれていないかチェック
'''

def checks(filepath):
    print repr(open(filepath, 'rb').read(200)) # dump 1st 200 bytes of file
    data = open(filepath, 'rb').read()
    print data.find('\x00')
    print data.count('\x00')

def fixCVS(filepath):
    fi = open(filepath, 'rb')
    data = fi.read()
    fi.close()
    fo = open('fixedCVS.csv', 'wb')
    fo.write(data.replace('\x00', ''))
    fo.close()
    
if __name__ == '__main__':
    filepath = r'C:\WORK\MalList\Output\ShinoBOT\-K-W7X64A-192.168.12.56-2015-01-10.log'
    #checks(filepath)
    fixCVS(filepath)
    
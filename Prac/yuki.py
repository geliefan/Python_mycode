# -*- coding=utf-8 -*-
import urllib2
import time
import math

def getval(DB,INDEX):
  return urllib2.urlopen("http://salvageon.textfile.org/?db="+str(DB)+"&index="+str(INDEX))
DB = 1
INDEX = 100000
while 1:
  vals1 = getval(DB,INDEX)
  vals2 = getval(DB,INDEX+1)
  val1 = vals1.read().split(" ") #文字列をくぎる
  val2 = vals2.read().split(" ")
  #val3 = vals[2].read().split(" ")
  #val4 = vals[3].read().split(" ")
  slice1 = val1[2][1:]
  slice2 = val2[2][1:]
  #slice3 = val3[2][1:]
  #slice4 = val4[2][1:]
  key1 = long(slice2)-long(slice1)
  #key2 = long(slice4)-long(slice3)
  #key = key2 - key1
  if key1 >0 :
    print long(math.log10(key1)+1),
  else :
    print "LESS"
  print key1
  INDEX = INDEX+1
  vals=[]

print "END"

# -*- coding: utf-8 -*-
import os

def test(num_1, num_2, operation):

  if operation == 1:
    print "足し算開始"
    print num_1 + num_2

  elif operation == 2:
    print "引き算開始"
    print num_1 - num_2

  elif operation == 3:
    print "掛け算開始"
    print num_1 * num_2

  elif operation == 4:
    print "割り算開始"
    print num_1 / num_2

  else:
    print '不明なオペレーション指定'

if __name__ == "__main__":
  test(100, 10, 3)
  print os.sep
  print os.pathsep
  print os.extsep

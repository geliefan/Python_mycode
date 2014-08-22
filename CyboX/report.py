# -*- coding: utf-8 -*-
"""
CybOX文書の作成．
事前に定義されたオブジェクトとアクションをいれこんでいく形式か？
"""

'''
2014/08/22
１．検索（指定）したファイル情報をXML化する
２．XML情報からRDFに変換する
３．オントロジ？
'''
import sys
import cybox
import os
import datetime

def main():
  NS = cybox.utils.Namespace("http://example.com/","kont")
  cybox.utils.set_id_namespace(NS)
  #readObserve = Observables()

  #ファイル情報を読み取る
  fpath = r'C:\Users\Makoto\Downloads\KanColleViewer-ver.2.6\KanColleViewer ver.2.6\KanColleViewer.exe'
  file_info = os.stat(fpath)
  print file_info
  last_modified = file_info.st_mtime
  print(last_modified)
  dt = datetime.datetime.fromtimestamp(last_modified)
  print(dt.strftime("%Y-%m-%d %H:%M:%S"))  # Print最終更新日時

if __name__ == '__main__':
  main()

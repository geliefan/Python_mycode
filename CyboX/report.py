# -*- coding: utf-8 -*-
"""
CybOX文書の作成．
事前に定義されたオブジェクトとアクションをいれこんでいく形式か？
→各種情報取得し，取得情報に合わせたオブジェクト/アクション検索，observableに挿入
1.検索（指定）したファイル情報を取得
2.CybOX文書（XML化する）
3.XML情報からRDFに変換する
4.オントロジ作成？
"""

'''
from onPC
・ネットワーク情報
・PC情報
  PC名，OS，machine,etc
from CAPLogger
・ファイル名/型/パス
・通信元IP/ポート，通信先IP/ポート
'''
import sys
import cybox
import os
import datetime
import platform
import wx
from cybox.objects.file_object import File,FilePath
from cybox.objects import system_object
from cybox.core import Observable, Observables, action, AssociatedObject, action_reference,event,object
import netifaces #ネットワーク情報
from cybox.objects.address_object import Address


#各種ファイルパス
fpath = r'C:\RDFsample\ADD_0.png'  #自宅PC
pfile = r"C:\WORK\GitHub\Python_mycode\CyboX\seccon2014.pcap"
last_modified = ""
sys_info= ""
dt = ""

#ファイル情報を読み取る
def mininginfo():
  file_info = os.stat(fpath)
  print "file_info:",file_info
  last_modified = file_info.st_mtime
  dt = datetime.datetime.fromtimestamp(last_modified)
  print "last_modified_time:",dt.strftime("%Y-%m-%d %H:%M:%S")  # Print最終更新日時

  #OS等paltform情報を読み取る（PC固有情報になるのか？）
  #参考？：http://docs.python.jp/2.6/library/platform.html
  print 'machine:',
  print platform.machine()
  print platform.node()
  print platform.platform(0,0)
  print platform.processor()
  print platform.python_build()
  sys_info =platform.system()
  sys_re = platform.release()
  sys_ver = platform.version()
  print sys_info,sys_re,sys_ver
  print platform.system_alias(sys_info, sys_re, sys_ver)
  print platform.uname()

  print os.getpid()

def print_dict(d):
        for item in d or []:
            print '\t\t',
            for key, value in item.items():
                print '%s: %s,' % (key, value),
            print ''


def pc2cybox(capob):
  NS = cybox.utils.Namespace("http://example.com/","lift_s")
  cybox.utils.set_id_namespace(NS)
  pc = system_object.System()
  pc_sys = system_object.OS()
  #pc_sys.platform = platform.system()
  #pc_sys.os =
  #pc_sys.prcessor =
  #pc_sys.hostname =
  pc_sys.network_interface_list = system_object.NetworkInterfaceList()
  pc_net = system_object.NetworkInterface()
  #ネットワーク情報の取得
  pc_adress = system_object.IPInfo()
  print '-------------'
  for iface_name in netifaces.interfaces():
    iface_data = netifaces.ifaddresses(iface_name)
    print 'Interface: %s' % (iface_name, )
    inter_name = iface_name

    mac = iface_data.get(netifaces.AF_LINK)
    for add in mac or []:
      for key, value in add.items():
          print "mac",
          print '%s: %s,' % (key, value),
          ad1 = Address(value,Address.CAT_MAC)
          ad1.vlan_name
      print ''

    ipv4 = iface_data.get(netifaces.AF_INET)
    for add in ipv4 or []:
      for key, value in add.items():
          print "ipv4",
          print '%s: %s,' % (key, value),
          ad1 = Address(value,Address.CAT_IPV4)
      print ''

    ipv6 = iface_data.get(netifaces.AF_INET6)
    for add in ipv6 or []:
      for key, value in add.items():
          print 'ipv6',
          print '%s: %s,' % (key, value),
          ad1 = Address(value,Address.CAT_IPV6)
      print ''
  pc_net.ip_list = system_object.IPInfoList(iplist)

  ls = [capObser]
  for ob in ls:
    capob.add(ob)
  return capob

def cap2cybox(capob):
  NS = cybox.utils.Namespace("http://example.com/","lift_s")
  cybox.utils.set_id_namespace(NS)

  #ファイル情報
  files = File()
  root, ext = os.path.splitext(fpath)
  path = FilePath(root)
  files.file_name = os.path.basename(fpath)
  files.file_path = path
  files.file_extension = ext

  capObser = Observable(files)
  capObser.description = u'ファイル情報'
  ls = [capObser]
  for ob in ls:
    capob.add(ob)
  return capob

if __name__ == '__main__':
  log = Observables()
  mininginfo()
  log = pc2cybox(log)    #PC情報の追加
  log = cap2cybox(log)   #CAPLogger情報の追加
  xml = open("lifts_pc.xml","w")
  xml.write(log.to_xml())
  xml.close()
  print log.to_xml()

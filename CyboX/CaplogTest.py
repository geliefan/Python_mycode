# -*- coding=utf-8 -*-
import codecs
import csv
import sys
import cybox.bindings.cybox_core as cybox_core_binding
from cybox.core import *
import cybox.utils
#file:FileObject
from cybox.objects.file_object import File,FilePath
from cybox.objects.process_object import *
#domain:domain_nameObject
from cybox.objects.domain_name_object import DomainName
from cybox.objects.network_socket_object import *
#code:CodeObject 未実装？
from cybox.objects.code_object import Code
from Recoder import *

OB = Observables()

#CaybOX変換，引数：１行のリスト
def cap2cybox(row):
  NS = cybox.utils.Namespace("http://LIFT-S.com/","example")
  cybox.utils.set_id_namespace(NS)


  if row[7] == "PROCESS_QUIT":
    #read 8
    P = Process()
    P.pid = int(row[8])
    POB = Object(P)
    POb = Observable(POB)
    POb.description = "This type is PROCESS_QUIT"
    OB.add(POb)

  elif row[7] == "PROCESS_MODLOAD":
    #read 8,10
    P = Process()
    P.pid = int(row[8])
    F = File()
    F.file_path = row[10]
    OB_P = Object(P)
    OB_F = Object(F)
    OB_P.add_related(F,"tes1","tes2")
    OB_F.add_related(P,"tes3","tes4")
    OB.add(OB_P)
    OB.add(OB_F)

  elif row[7] == "PROCESS_LAUNCH":
    #read 8,9,10,11
    P = Process()
    P.pid = int(row[8])
    P.parent_pid = int(row[9])
    F = File()
    F.file_path = row[10]

  elif row[7] == "NETWORKV4":
    #read 8,12,13,14,15,16
    net = NetworkConnection()
    net.layer3_protocol = "IPv4"
    # Sorce socket
    Add = Address()
    Add.address_value = row[12]
    Por = Port()
    Por.port_value = row[13]
    Soc = SocketAddress()
    Soc.ip_address = Add
    Soc.port = Por
    net.source_socket_address =Soc
    # destination socket
    Add = Address()
    Add.address_value = row[14]
    Por = Port()
    Por.port_value = row[15]
    Des = SocketAddress()
    Des.ip_address = Add
    Des.port = Por
    net.destination_socket_address = Des
    NetOB = Object(net)
    NetOb = Observable(NetOB)
    OB.add(NetOb)

  elif row[7] == "NETWORKV6":
    #read 8,12,13,14,15,16
    net = NetworkConnection()
    net.layer3_protocol = "IPv6"
    # Sorce socket
    Add = Address()
    Add.address_value = row[12]
    Por = Port()
    Por.port_value = row[13]
    Soc = SocketAddress()
    Soc.ip_address = Add
    Soc.port = Por
    net.source_socket_address =Soc
    # destination socket
    Add = Address()
    Add.address_value = row[14]
    Por = Port()
    Por.port_value = row[15]
    Des = SocketAddress()
    Des.ip_address = Add
    Des.port = Por
    net.destination_socket_address = Des
    NetOB = Object(net)
    NetOb = Observable(NetOB)
    OB.add(NetOb)
  else:
    print "New TYPE:",row[7]




with open('hoge.log','rb') as f:
    sr = Recoder(f, 'utf-16', 'utf-8')
    xml = open("CapLogger.xml","w")

    for row in csv.reader(sr):
        cap2cybox(row)
    xml.write(OB.to_xml())
    xml.close()
    print OB.to_xml(include_namespaces = False)

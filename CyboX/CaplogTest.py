# -*- coding=utf-8 -*-
import codecs
import csv
import sys
import datetime
import cybox.bindings.cybox_core as cybox_core_binding
from cybox.core import *
from cybox.common import *
import cybox.utils
#file:FileObject
from cybox.objects.file_object import File,FilePath
from cybox.objects.process_object import *
#domain:domain_nameObject
from cybox.objects.domain_name_object import DomainName
from cybox.objects.network_socket_object import *
from cybox.objects.win_process_object import *

from cybox.objects.code_object import Code
from Recoder import *
#debug
from cybox.objects.email_message_object import EmailMessage

OB = Observables()
#CaybOX変換，引数：１行のリスト
def cap2cybox(row):
  NS = cybox.utils.Namespace("http://LIFT-S.com/","example")
  cybox.utils.set_id_namespace(NS)
  
  #時間
  dates = ""
  for d in range(7):
      dates += row[d]+"-"
  dd = datetime.strptime(dates,'%Y-%m-%d-%H-%M-%S-%f-')
  
  if row[7] == "PROCESS_QUIT":
    #read 8
    PQ = Process()
    PQ.pid = int(row[8])
    '''
         アクションの記述
    '''
    #参照関係
    ao_p = action.AssociatedObject(PQ)
    #code_ao = AssociatedObject(code)
    aos1 = action.AssociatedObjects([ao_p])
    #Modular Load
    a = action.Action()
    a.timestamp = dd
    a.type_ = "Kill"
    a.name = "Kill Process"
    a.desctiption = StructuredText("This type is PROCESS_QUIT")
    a.associated_objects = aos1
    #アクションをイベントにセット
    aa = action.Actions([a])
    e = event.Event()
    e.actions = aa
    e.type_ = "Process Mgt"
    OBs = Observable()
    OBs.event = e
    OBs.date = dd
    OB.add(OBs)   
    
  elif row[7] == "PROCESS_MODLOAD":
    #read 8,10
    PM = Process()
    PM.pid = int(row[8])
    #WPOB = WinProcess(PM)
    F = File()
    F.file_path = row[10]    
    '''
         アクションの記述
    '''
    #参照関係
    ao_p = action.AssociatedObject(PM)
    ao_F = action.AssociatedObject(F)
    #code_ao = AssociatedObject(code)
    aos1 = action.AssociatedObjects([ao_p,ao_F])
    #Modular Load
    a = action.Action()
    a.timestamp = dd
    a.type_ = "Load"
    a.name = "Load Module"
    a.desctiption = "MODLOAD"
    a.associated_objects = aos1
    #アクションをイベントにセット
    aa = action.Actions([a])
    e = event.Event()
    e.actions = aa
    e.type_ = "Process Mgt"
    OBs = Observable()
    OBs.event = e
    #OBs.object_= Object(PM)
    #OB_F = Object(F)
    #OB_P.add_related(F,"Loaded_into","tes2")
    #OB_F.add_related(PM,"Loaded_From","tes4") #Object作成が必要が検討が必要
    OB.add(OBs)
    #OB.add(OB_F)
    
  elif row[7] == "PROCESS_LAUNCH":
    #read 8,9,10,11
    PL = Process()
    PL.pid = int(row[8])
    PL.parent_pid = int(row[9]) #実行時は必ずPPIDは存在する？
    PL.start_time = dd
    #WPOB = WinProcess(PL)
    #OB_P = Object(PL)
    F = File()
    F.file_path = row[10]
    #OB.add(OB_P)
    '''
         アクションの記述
    '''
    #参照関係
    ao_p = action.AssociatedObject(PL)
    ao_F = action.AssociatedObject(F)
    #code_ao = AssociatedObject(code)
    aos1 = action.AssociatedObjects([ao_p,ao_F])
    #Modular Load
    a = action.Action()
    a.timestamp = dd
    a.type_ = "Start"
    a.name = "Open Process"
    ActArg = ActionArgument()
    ActArg.argument_name = "Command"
    ActArg.argument_value = row[11]
    a.action_arguments = ActionArguments(ActArg)
    a.desctiption = "LAUNCH"
    a.associated_objects = aos1
    #アクションをイベントにセット
    aa = action.Actions([a])
    e = event.Event()
    e.actions = aa
    e.type_ = "Process Mgt"
    OBs = Observable()
    OBs.event = e
    #OB_F = Object(F)
    OB.add(OBs)
    #OB.add(OB_F)

  elif row[7] == "NETWORKV4":
    #read 8,12,13,14,15,16
    P = Process()
    P.pid = int(row[8])
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
    '''
            アクションの記述
    '''
    #参照関係
    ao_s = AssociatedObject(net)
    #ao_s.association_type = "Initiating"
    ao_p = AssociatedObject(P)
    #ao_p.association_type = "Affected"
    #code_ao = AssociatedObject(code)
    aos1 = action.AssociatedObjects([ao_s,ao_p])
    #Modular Load
    a = action.Action()
    a.timestamp = dd
    a.type_ = "Connect"
    a.name = "Connect to IP"
    a.desctiption = StructuredText("This type is NETWORKV4")
    a.associated_objects = aos1
    #アクションをイベントにセット
    aa = action.Actions([a])
    e = event.Event()
    e.actions = aa
    e.type_ = "Process Mgt"
    OBs = Observable()
    OBs.event = e
    OB.add(OBs)  


  elif row[7] == "NETWORKV6":
    #read 8,12,13,14,15,16
    P = Process()
    P.pid = int(row[8])
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
    '''
            アクションの記述
    '''
    #参照関係
    ao_s = AssociatedObject(net)
    #ao_s.association_type = "Initiating"
    ao_p = AssociatedObject(P)
    #ao_p.association_type = "Affected"
    aos1 = action.AssociatedObjects([ao_s,ao_p])
    #Modular Load
    a = action.Action()
    a.timestamp = dd
    a.type_ = "Connect"
    a.name = "Connect to IP"
    a.desctiption = StructuredText("This type is NETWORKV4")
    a.associated_objects = aos1
    #アクションをイベントにセット
    aa = action.Actions([a])
    e = event.Event()
    e.actions = aa
    e.type_ = "Process Mgt"
    OBs = Observable()
    OBs.event = e
    OB.add(OBs)  

  else:
    print "New TYPE:",row[7]


if __name__ == '__main__':
    with codecs.open(r'sample.log', 'r',encoding="utf-16le") as f:
    #with open("sample.log",'rb') as f:
        #sr = Recoder(f, 'utf-16', 'utf-8')
        sr = f
        xml = open("shinoBOT_ver02.xml","w")
        for row in csv.reader(sr):
            cap2cybox(row)

        xml.write(OB.to_xml())
        xml.close()
    print "done"
    #print OB.to_xml(include_namespaces = False)

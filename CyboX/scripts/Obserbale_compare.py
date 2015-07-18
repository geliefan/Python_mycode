# -*- coding=utf8 -*-
'''
Created on 2015/02/17

@author: Makoto
'''
# Observableを１つづつ取り出してObservable同士で比較する
import cybox.bindings.cybox_core as cybox_core_binding
from cybox.core import Observables, Observable, Event, Action
from cybox.bindings import cybox_core
from dpkt.asn1 import NULL
from IPython.core.magic_arguments import kwds
import time,os

Path_Malware2 = r"C:\WORK\GitHub\Python_mycode\CyboX\shinoBOT_ver02.xml"
Path_Malware1 = r"C:\WORK\GitHub\Python_mycode\CyboX\Logs\VirusShare_001dd76872d80801692ff942308c64e6.xml"
Path_Malware3 = r"C:\WORK\GitHub\Python_mycode\CyboX\Logs\VirusShare_0cf9e999c574ec89595263446978dc9f.xml"
MalwareList = [Path_Malware1,Path_Malware2,Path_Malware3]

#Path_Log     = r"C:\WORK\GitHub\Python_mycode\CyboX\ShinoBOTSuite_rawLog-K-W7X64A-192.168.1.80-2015-02-19.xml"
#Path_Log     = r"C:\WORK\GitHub\Python_mycode\CyboX\Logs\VirusShare_0cf9e999c574ec89595263446978dc9f.xml"
Path_Log     = r"C:\WORK\GitHub\Python_mycode\CyboX\-K-W7X64A-192.168.1.20-2015-02-17.xml"



class Bunch(object):
    def __init__(self, **kwds):
        self.__dict__.update(kwds)

def parse(filepath):
    xml = open(filepath,"r")
    par = cybox_core_binding.parse(xml)
    obs = Observables.from_obj(par)
    return obs

# パターンとなる要素（文字列）を取り出してリストに変換
def cyboxpop(dict):
    pros    =   []
    actarg  =   []
    if dict.has_key("event"):
        for num in range(len(dict["event"]["actions"])):
            if dict["event"]["actions"][num]["name"] == "Open Process":
                actname =   dict["event"]["actions"][num]["name"]
                
                if dict["event"]["actions"][num].has_key("action_arguments"):
                    for arg in range(len(dict["event"]["actions"][num]["action_arguments"])):
                        actarg.append(dict["event"]["actions"][num]["action_arguments"][arg]["argument_value"])
            
                for pro in range(len(dict["event"]["actions"][num]["associated_objects"])):
                    actpro = dict["event"]["actions"][num]["associated_objects"][pro]["properties"]
                    pros.append(actpro)
                args = Bunch(ActName=actname, ActArg=actarg, Propertys=pros)
                return args
            else:
                """
                #MODLOADを入れるにはプロセスツリーの解析も同時にする必要がある
                actname =   dict["event"]["actions"][num]["name"]
                
                if dict["event"]["actions"][num].has_key("action_arguments"):
                    for arg in range(len(dict["event"]["actions"][num]["action_arguments"])):
                        actarg.append(dict["event"]["actions"][num]["action_arguments"][arg]["argument_value"])
            
                for pro in range(len(dict["event"]["actions"][num]["associated_objects"])):
                    actpro = dict["event"]["actions"][num]["associated_objects"][pro]["properties"]
                    pros.append(actpro)
                args = Bunch(ActName=actname, ActArg=actarg, Propertys=pros)
                return args
                """
                return None
    else:
        return None

def main(Path_Malware):
    malobs = Observables()
    logobs = Observables()
    Malware = parse(Path_Malware)
    Log     = parse(Path_Log)
    CONFIDENCE = 0  #一致した数

    mallist = []
    loglist = []
    m = 0
    key = 0
    
    for ob in Malware:
        args = cyboxpop(ob.to_dict())
        if args is not None:
            mallist.append(args)
            #print args.ActArg
            malobs.add(ob)
    
    for ob in Log:
        args = cyboxpop(ob.to_dict())
        if args is not None:
            loglist.append(args)
            logobs.add(ob)
    
    #print "mallist_count:", len(mallist)
    #print "loglist_count:", len(loglist)
    
    '''
    for mal_num in range(len(mallist)):
        #if loglist[log_num]["event"]["actions"][0]["name"] == mallist[0]["event"]["actions"][0]["name"]:
        cyboxpop(mallist[mal_num])           
        
    #print mallist
    '''
    print "------------------",os.path.basename(Path_Malware),"-------------------"
    
    for n in range(len(loglist)):
        #print "Log:",n,loglist[n].ActArg,loglist[n].Propertys,len(loglist[n].Propertys)
        #print "[1]:",mallist[1].ActArg,mallist[1].Propertys[1]
        #if loglist[n].ActName == mallist[1].ActName and loglist[n].ActArg == mallist[1].ActArg: #ShinoBOT.exe
        #if loglist[n].ActName == mallist[1].ActName and loglist[n].Propertys[1] == mallist[1].Propertys[1]: #SHinoBOTSuiteで偽装したファイル
        #if len(loglist[n].Propertys) > 1:
        if loglist[n].Propertys[1] == mallist[0].Propertys[1]:
            #if len(loglist)-n-len(loglist) < 0 : break
            l=0
            #print "POST!"
            while True:
                if len(mallist) < m+1 or len(loglist) < n+l+1:
                    key = n+l
                    break 
                if key < n+l and loglist[n+l].Propertys[1] == mallist[m].Propertys[1]:
                    print "Log[",n+l,"]:",loglist[n+l].ActArg,loglist[n+l].Propertys
                    print "Mal[",m,"]:",mallist[m].ActArg,mallist[m].Propertys
                    CONFIDENCE += 1
                    l +=1
                    m +=1

                else :
                    l +=1

    
    #print logobs.to_xml()
    print "パターン一致数:",CONFIDENCE
    print "マルウェアプロセス数:",len(mallist)
    print "ログプロセス数:",len(loglist)
    print "パターン一致割合：",float(CONFIDENCE)/len(mallist)
    
    
    
if __name__ == '__main__':
    for path in MalwareList:
        main(path)

    
    

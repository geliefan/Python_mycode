# -*- coding=utf-8 -*-
'''
@author: Makoto
'''

import sys
import cybox.bindings.cybox_core as cybox_core_binding
from cybox.bindings.process_object import *
from  cybox.core import Observables
import maec.utils
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
#code:CodeObject 未実装？
from cybox.objects.code_object import Code
from Recoder import *
import maec.package.malware_subject
import maec.bindings.maec_package as package_binding
import cybox.bindings.process_object as process_binding
from maec.package.package import Package
from maec.package.malware_subject import FindingsBundleList
from maec.bundle.bundle import Bundle
from maec.bindings import maec_bundle
from maec.package import malware_subject

# パーサ
def parse(xml_file):
    obs_obj = cybox_core_binding.parse(xml_file) # create binding object from xml file
    obs = Observables.from_obj(obs_obj) # convert binding object into python-cybox object
    #pro = process_binding.(xml_file)
    #p = Process.from_obj(pro)
    #print p.pid    
    return obs

def cybox_s(cyboxs):
    for n in cyboxs:
        #辞書形式で取得
        ob = n.to_dict()
        if ob["event"]["actions"][0]["name"] == "Open Process":
            print "Log:"
            if "action_arguments" in ob["event"]["actions"][0]: 
                print "argument",ob["event"]["actions"][0]["action_arguments"][0]["argument_value"]
            if "properties" in ob["event"]["actions"][0]["associated_objects"][0]:
                f_path = ob["event"]["actions"][0]["associated_objects"][1]["properties"]["file_path"]
                print "file_path:",f_path
                pid = ob["event"]["actions"][0]["associated_objects"][0]["properties"]["pid"]
                print "PID",pid
                ppid = ob["event"]["actions"][0]["associated_objects"][0]["properties"]["parent_pid"]
                print "PPID:",ppid
                dict = {"parent_pid":ppid,"pid":pid}
                p = Process.from_dict(dict)
                print p.pid
                
def maec_s(maecs):
    print "maec"
    maec_obj = package_binding.parse(maecs)
    obs = Package.from_obj(maec_obj)
    pac = Package(obs)
    dic = pac.to_dict()
    print "name:",dic["id"]["malware_subjects"][0]["findings_bundles"]["bundle"][0]["process_tree"]["root_process"]["name"]
    print "pid:",dic["id"]["malware_subjects"][0]["findings_bundles"]["bundle"][0]["process_tree"]["root_process"]["pid"]
    print "spawned_process:",dic["id"]["malware_subjects"][0]["findings_bundles"]["bundle"][0]["process_tree"]["root_process"]["spawned_process"]
    print "id:",dic["id"]["malware_subjects"][0]["findings_bundles"]["bundle"][0]["process_tree"]["root_process"]["id"]
    
    
    #fnd = maec_bundle.parseLiteral(maecs)
    #obs_obj = cybox_core_binding.parse(xml_file) # create binding object from xml file
    #print obs_obj.Malware_Subjects
    #obs = Observables.from_obj(obs_obj) # convert binding object into python-cybox object
    #obs = maec.package.malware_subject.MalwareSubject.from_obj(obs_obj)

                    
def main():
    xml_file = open("shinoBOT.xml", "r")
    cyboxs = parse(xml_file)
    cybox_s(cyboxs)
    #maecs = open("MalAnalyze_ShinoBOT.xml", "r")
    #maec_s(maecs)

    

if __name__ == '__main__':
    main()
        
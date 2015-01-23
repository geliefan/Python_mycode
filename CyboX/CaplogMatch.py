# -*- coding=utf-8 -*-
'''
@author: Makoto
'''

import sys
import cybox.bindings.cybox_core as cybox_core_binding
from cybox.bindings.process_object import *
from  cybox.core import Observables

# パーサ
def parse(xml_file):
    print "start"
    obs_obj = cybox_core_binding.parse(xml_file) # create binding object from xml file
    obs_s = cybox_core_binding.ObservableType(obs_obj.get_Observable())
    
    print obs_s
    ls = ProcessObjectType.get_Child_PID_List(obs_s.get_Event())
    print "getPID"
    print ls
    obs = Observables.from_obj(obs_obj) # convert binding object into python-cybox object
    return obs

def main():
    xml_file = open("CapLogger.xml", "r")
    observables = parse(xml_file) 
    #print observables.to_dict() # example to_dict() call on returned object

if __name__ == '__main__':
    main()
        
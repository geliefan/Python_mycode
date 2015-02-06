'''
Created on 2015/01/29

@author: Makoto
'''

import sys
import cybox.bindings.cybox_core as cybox_core_binding
import maec.utils as maec_utils
from  cybox.core import Observables
import xml.etree.ElementTree as ET

def parse(cybox_file):
    observables_obj = cybox_core_binding.parse(cybox_file) # create binding object from xml file
    observables = Observables.from_obj(observables_obj) # convert binding object into python-cybox object
    return observables

def main():
    cybox_file = r"shinoBOT.xml"
    maec_file = r"MalAnalyze_ShinoBOT.xml"
    observables = parse(cybox_file)
    print "CybOX"
    print observables # example to_dict() call on returned object
    
    maec_obj = maec_utils.parser.EntityParser.parse_xml_to_obj(maec_file)
    #maec_obs = parse(maec_file) 
    print "MAEC"
    print maec_obj.get_Malware_Subjects()

def test():
    tree = ET.parse('shinoBOT.xml')
    root = tree.getroot()
    lists = root.findall(".//event")
    for ele in lists:
        print ele.text
        
if __name__ == '__main__':
    test()
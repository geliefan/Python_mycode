# -*- coding: utf-8 -*-
# LastlineのLogを記述．
# sample.pyを流用

# プロセス（ツリー） in maecBundle
# analysys in Package
import os
from datetime import datetime
import json
import pytz
from cybox.objects.win_mutex_object import WinMutex
from cybox.objects.dns_query_object import DNSQuery, DNSQuestion,\
    DNSResourceRecords
from cybox.core import AssociatedObjects, AssociatedObject, Object, AssociationType
from cybox.common import Hash, HashList
from cybox.objects.file_object import File
from cybox.utils import Namespace
import maec.utils
from maec.package.package import Package
from maec.package.malware_subject import MalwareSubject
from maec.package.analysis import Analysis
from maec.bundle.bundle import Bundle, ActionList, BehaviorList
from maec.bundle.malware_action import MalwareAction
from maec.bundle.process_tree import ProcessTree, ProcessTreeNode
from cybox.objects.win_executable_file_object import WinExecutableFile
from cybox.objects.win_file_object import WinFile
from cybox.common import ToolInformation, VocabString
from cybox.objects import win_registry_key_object, library_object
from cybox.core.action import Action
from cybox.bindings import win_file_object
from cybox.objects.uri_object import URI
from cybox.objects.dns_record_object import DNSRecord
from cybox.objects.address_object import Address
from cybox.objects.library_object import Library
from cybox.common.properties import UnsignedLong, DateTime, PositiveInteger
from cybox.objects.win_process_object import WinProcess
from cybox.objects.http_session_object import HTTPSession,\
    HTTPResponseHeaderFields, HTTPResponseHeader, HTTPServerResponse,\
    HTTPClientRequest, HTTPRequestHeader, HTTPRequestHeaderFields, HTTPMessage,\
    HostField, HTTPStatusLine, HTTPRequestLine, HTTPRequestResponse
from cybox.objects.network_connection_object import NetworkConnection,\
    Layer7Connections
from cybox.objects.port_object import Port
import cybox
from maec.bundle.behavior import Behavior, BehavioralActions, BehavioralAction
from cybox.core.observable import Observables, Observable
from cybox.core.event import Event

class mkSubject():
    # サンプルの名前空間に（自動ID生成用の）IDジェネレータクラスをインスタンス化
    NS = Namespace("http://lastline.com/", "example")
    maec.utils.set_id_namespace(NS)
    OB = Observables()

    # インスタンス化：Bundle, Package, MalwareSubject, Analysis classes
    bundle = Bundle(defined_subject=False)
    package = Package()
    subject = MalwareSubject()
    analysis = Analysis()


    # Populate the Analysis with the metadata relating to the Analysis that was performed
    analysis.method = "dynamic"
    analysis.type_ = "triage"
    analysis.set_findings_bundle(bundle.id_)
    t = ToolInformation()
    t.name = "Lastline"
    t.vendor = "n_SCSK"
    analysis.add_tool(t)

    # ActionList
    # BehabioralList
    b = Behavior()
    ba = BehavioralAction()
    bas = BehavioralActions()
    #ba.behavioral_ordering
    bas.action = ba

    
    # xmlで記述
    def maecwrite(self,actions,behavior):
        # パッケージへMalwareSubjectを追加
        self.package.add_malware_subject(self.subject)
        # バンドルへActionを追加
        self.bundle.actions = actions
        self.bundle.behaviors = behavior
        # bundle.add_behavior(behavior)
        # Add the Bundle to the Malware Subject
        # Malware Subjectへバンドルを追加
        self.subject.add_findings_bundle(self.bundle)
        self.subject.add_analysis(self.analysis)

        # Export the Package Bindings Object to an XML file and use the namespaceparser for writing out the namespace definitions
        self.package.to_xml_file('lastline_test.xml', {"http://lastline_test/":"LIFT-S"})
        print "Wrote to lastline_test.xml"
        
    def cyboxwrite(self,file):
        file.write(self.OB.to_xml())
    
    def addSubject_cybox(self,actions):
        e = Event()
        e.actions = actions
        e.description = "Add Subject"
        OBs = Observable()
        OBs.event = e
        self.OB.add(OBs)
            
# registry_reads
def registry_reads(registry):
    a = MalwareAction()
    ao = AssociatedObject()
    a.name = "Read Registry Key Value"
    a.type_= "Read"
        
    ao.properties = win_registry_key_object.WinRegistryKey()
    ao.properties.key = registry["key"]
    
    if registry.has_key("data"):
        value = win_registry_key_object.RegistryValue()
        if registry.has_key("value"):
            value.name = registry["value"]
        value.data = registry["data"]
        values = win_registry_key_object.RegistryValues([value])
        ao.properties.values = values
    ao.association_type = VocabString()
    ao.association_type.value = ""
    ao.association_type.xsi_type = "maecVocabs:ActionObjectAssociationTypeVocab-1.0"
    a.associated_objects = AssociatedObjects()
    a.associated_objects.append(ao)
    return a

def registry_writes(registry):
    a = MalwareAction()
    ao = AssociatedObject()
    a.name = "Modify Registry Key Value"
    a.type_= "Modify"
         
    ao.properties = win_registry_key_object.WinRegistryKey()
    ao.properties.key = registry["key"]
    
    if registry.has_key("data"):
        value = win_registry_key_object.RegistryValue()
        value.name = registry["value"]
        value.data = registry["data"]
        values = win_registry_key_object.RegistryValues([value])
        ao.properties.values = values
    
    a.associated_objects = AssociatedObjects()
    a.associated_objects.append(ao)
    return a

'''
"file_reads": [
                    {
                        "abs_path": "C:\\WINDOWS\\system32\\IMM32.DLL", 
                        "filename": "C:\\WINDOWS\\system32\\IMM32.DLL"
                    }, 
                    {
                        "abs_path": "C:\\WINDOWS\\system32\\MSCTF.dll", 
                        "filename": "C:\\WINDOWS\\system32\\MSCTF.dll"
                    }, 
                    {
                        "abs_path": "C:\\WINDOWS\\system32\\IPHLPAPI.DLL", 
                        "filename": "C:\\WINDOWS\\system32\\IPHLPAPI.DLL"
                    }, 
                    {
                        "abs_path": "C:\\WINDOWS\\system32\\ws2_32.dll", 
                        "filename": "C:\\WINDOWS\\system32\\WS2_32.dll"
                    }, 
                    {
                        "abs_path": "C:\\WINDOWS\\System32\\winrnr.dll", 
                        "filename": "C:\\WINDOWS\\System32\\winrnr.dll"
                    }, 
                    {
                        "abs_path": "C:\\WINDOWS\\system32\\Apphelp.dll", 
                        "filename": "C:\\WINDOWS\\system32\\Apphelp.dll"
                    }, 
                    {
                        "abs_path": "C:\\WINDOWS\\system32\\NETAPI32.dll", 
                        "filename": "C:\\WINDOWS\\system32\\NETAPI32.dll"
                    }, 
                    {
                        "abs_path": "C:\\WINDOWS\\system32\\winhttp.dll", 
                        "filename": "C:\\WINDOWS\\system32\\winhttp.dll"
                    }, 
                    {
                        "filename": "\\Device\\Ip"
                    }, 
                    {
                        "abs_path": "C:\\WINDOWS\\system32\\rasadhlp.dll", 
                        "filename": "C:\\WINDOWS\\system32\\rasadhlp.dll"
                    }, 
                    {
                        "abs_path": "C:\\WINDOWS\\system32\\msiexec.exe", 
                        "filename": "C:\\WINDOWS\\system32\\msiexec.exe"
                    }, 
                    {
                        "abs_path": "C:\\WINDOWS\\system32\\CRYPT32.dll", 
                        "filename": "C:\\WINDOWS\\system32\\crypt32.dll"
                    }, 
                    {
                        "abs_path": "C:\\WINDOWS\\system32\\MSASN1.dll", 
                        "filename": "C:\\WINDOWS\\system32\\MSASN1.dll"
                    }, 
                    {
                        "abs_path": "C:\\WINDOWS\\system32\\WS2HELP.dll", 
                        "filename": "C:\\WINDOWS\\system32\\WS2HELP.dll"
                    }, 
                    {
                        "abs_path": "C:\\Documents and Settings\\admin\\Application Data\\", 
                        "filename": "C:\\Documents and Settings\\admin\\Application Data\\"
                    }, 
                    {
                        "abs_path": "C:\\WINDOWS\\system32\\MSOERT2.dll", 
                        "filename": "C:\\WINDOWS\\system32\\MSOERT2.dll"
                    }, 
                    {
                        "abs_path": "C:\\WINDOWS\\System32\\wshtcpip.dll", 
                        "filename": "C:\\WINDOWS\\System32\\wshtcpip.dll"
                    }, 
                    {
                        "abs_path": "c:\\docume~1\\admin\\applic~1\\dfltprc.exe", 
                        "filename": "C:\\Documents and Settings\\admin\\Application Data\\dfltprc.exe"
                    }, 
                    {
                        "abs_path": "C:\\WINDOWS\\AppPatch\\AcGenral.DLL", 
                        "filename": "C:\\WINDOWS\\AppPatch\\AcGenral.DLL"
                    }, 
                    {
                        "abs_path": "C:\\WINDOWS\\system32\\", 
                        "filename": "C:\\WINDOWS\\system32\\"
                    }, 
                    {
                        "abs_path": "C:\\WINDOWS\\system32\\mswsock.dll", 
                        "filename": "C:\\WINDOWS\\system32\\mswsock.dll"
                    }, 
                    {
                        "filename": "Ip"
                    }, 
                    {
                        "abs_path": "C:\\WINDOWS\\system32\\INETCOMM.dll", 
                        "filename": "C:\\WINDOWS\\system32\\INETCOMM.dll"
                    }, 
                    {
                        "abs_path": "C:\\DOCUME~1\\admin\\LOCALS~1\\", 
                        "filename": "C:\\Documents and Settings\\admin\\Local Settings\\"
                    }, 
                    {
                        "abs_path": "C:\\WINDOWS\\system32\\hnetcfg.dll", 
                        "filename": "C:\\WINDOWS\\system32\\hnetcfg.dll"
                    }, 
                    {
                        "abs_path": "C:\\WINDOWS\\system32\\dnsapi.dll", 
                        "filename": "C:\\WINDOWS\\system32\\dnsapi.dll"
                    }, 
                    {
                        "ext_info": {
                            "size": "286720", 
                            "sha1": "716d5b16ca04b9ddccd4e005d42f79b463e3f31b", 
                            "file_info": "PE32 executable (GUI) Intel 80386, for MS Windows", 
                            "md5": "1e55393b9b0d10800d0b363ee13afc66"
                        }, 
                        "abs_path": "C:\\DOCUME~1\\admin\\LOCALS~1\\Temp\\msi62532.exe", 
                        "filename": "C:\\DOCUME~1\\admin\\LOCALS~1\\Temp\\msi62532.exe"
                    }, 
                    {
                        "filename": "\\Device\\NetBT_Tcpip_{45F45E56-3147-4AE0-802C-94D104C58A80}"
                    }, 
                    {
                        "abs_path": "C:\\WINDOWS\\system32\\adsldpc.dll", 
                        "filename": "C:\\WINDOWS\\system32\\adsldpc.dll"
                    }, 
                    {
                        "abs_path": "C:\\WINDOWS\\system32\\inetres.dll", 
                        "filename": "C:\\WINDOWS\\system32\\inetres.dll"
                    }, 
                    {
                        "abs_path": "C:\\WINDOWS\\system32\\ACTIVEDS.dll", 
                        "filename": "C:\\WINDOWS\\system32\\ACTIVEDS.dll"
                    }, 
                    {
                        "abs_path": "C:\\DOCUME~1\\admin\\", 
                        "filename": "C:\\Documents and Settings\\admin\\"
                    }, 
                    {
                        "filename": "\\Device\\Tcp"
                    }, 
                    {
                        "abs_path": "C:\\DOCUME~1\\admin\\LOCALS~1\\Temp\\", 
                        "filename": "C:\\Documents and Settings\\admin\\Local Settings\\Temp"
                    }, 
                    {
                        "abs_path": "C:\\WINDOWS\\system32\\cdosys.dll", 
                        "filename": "C:\\WINDOWS\\system32\\cdosys.dll"
                    }
                ]
'''

# file_reads
def file_reads(files):
    a = MalwareAction()
    ao = AssociatedObject()
    a.name = "Read File"
    a.type_ = "Read"

    ao.properties = WinFile()
    ao.properties.file_name = files["filename"]
    
    if files.has_key("ext_info"):
        ao.properties.full_path = files["abs_path"]
        ao.properties.size_in_bytes = UnsignedLong(files["ext_info"]["size"])
        hashs = []
        hashs.append(Hash(files["ext_info"]["sha1"]))
        hashs.append(Hash(files["ext_info"]["md5"]))
        ao.properties.hashes = HashList(hashs)
        ao.properties.file_format = files["ext_info"]["file_info"]
    elif files.has_key("abs_path"):
        ao.properties.full_path = files["abs_path"]
    
    a.associated_objects = AssociatedObjects()
    a.associated_objects.append(ao)
    return a

#  file_writes
def file_writes(files):
    a = MalwareAction()
    ao = AssociatedObject()
    a.name = "Write to File"
    a.type_ = "Write"

    ao.properties = WinFile()
    ao.properties.file_name = files["filename"]
    
    if files.has_key("ext_info"):
        ao.properties.full_path = files["abs_path"]
        ao.properties.size_in_bytes = UnsignedLong(files["ext_info"]["size"])
        hashs = []
        hashs.append(Hash(files["ext_info"]["sha1"]))
        hashs.append(Hash(files["ext_info"]["md5"]))
        ao.properties.hashes = HashList(hashs)
        ao.properties.file_format = files["ext_info"]["file_info"]
    elif files.has_key("abs_path"):
        ao.properties.full_path = files["abs_path"]
    
    a.associated_objects = AssociatedObjects()
    a.associated_objects.append(ao)
    return a
def file_delete(files):
    a = MalwareAction()
    ao = AssociatedObject()
    a.name = "Delete File"
    a.type_ = "Remove/Delete"

    ao.properties = WinFile()
    ao.properties.file_name = files["filename"]
    
    if files.has_key("ext_info"):
        ao.properties.full_path = files["abs_path"]
        ao.properties.size_in_bytes = UnsignedLong(files["ext_info"]["size"])
        hashs = []
        hashs.append(Hash(files["ext_info"]["sha1"]))
        hashs.append(Hash(files["ext_info"]["md5"]))
        ao.properties.hashes = HashList(hashs)
        ao.properties.file_format = files["ext_info"]["file_info"]
    elif files.has_key("abs_path"):
        ao.properties.full_path = files["abs_path"]
    
    a.associated_objects = AssociatedObjects()
    a.associated_objects.append(ao)
    return a

# loaded_libraries
def loaded_libraries(filenames):
    a = MalwareAction()
    ao = AssociatedObject()
    a.name = "Load Library"
    a.type_ = "Load"
    
    name, ext = os.path.splitext( os.path.basename(filenames["filename"]) )
    dic = {}
    dic['name'] = name
    dic['path'] = filenames["filename"]
    
    lib = Library.from_dict(dic)
    ao.properties = lib
    
    a.associated_objects = AssociatedObjects()
    a.associated_objects.append(ao)
    return a

def modified_libraries(filenames):
    a = MalwareAction()
    ao = AssociatedObject()
    a.name = "Load Library"
    a.type_ = "Modify"
    
    path, ext = os.path.splitext( os.path.basename(filenames["filename"]) )

    dic= {'name':filenames["filename"]}
    lib = Library.from_dict(dic)
    ao.properties = lib
    
    a.associated_objects = AssociatedObjects()
    a.associated_objects.append(ao)
    return a

"""
    process= {
        "bitsize": 32, 
        "executable": {
            "abs_path": "c:\\docume~1\\admin\\applic~1\\dfltprc.exe", 
            "filename": "C:\\Documents and Settings\\admin\\Application Data\\dfltprc.exe"
        }, 
        "process_id": 856, 
        "arguments": "\"C:\\Documents and Settings\\admin\\Application Data\\dfltprc.exe\"", 
        "analysis_subject_id": 2
    }, 
"""
# process : アクションじゃないので，あとで
def process_action(process):
    pass

"""
             "overview": {
                    "ext_info": {
                        "size": "106496", 
                        "sha1": "c010a0f25f9652e4b7d2fe562e0c6aefa72ca1a5", 
                        "file_info": "PE32 executable (GUI) Intel 80386, for MS Windows", 
                        "md5": "beaeaf220881d185b7fd1873bf87ed49"
                    }, 
                    "process": {
                        "bitsize": 32, 
                        "executable": {
                            "abs_path": "c:\\docume~1\\admin\\applic~1\\dfltprc.exe", 
                            "filename": "C:\\Documents and Settings\\admin\\Application Data\\dfltprc.exe"
                        }, 
                        "process_id": 856, 
                        "arguments": "\"C:\\Documents and Settings\\admin\\Application Data\\dfltprc.exe\"", 
                        "analysis_subject_id": 2
                    }, 
                    "id": 2, 
                    "analysis_reason": "Process started"
                }, 
"""
# overview : オブジェクトなのであとで（Processは上記と同一）
def overview(overview):
    pass

# "registry_deletions": [], 
def registry_deletions(registry):
    pass

'''
                "process_interactions": [
                    {
                        "operations": [
                            "create_thread", 
                            "create_process", 
                            "create_suspended"
                        ], 
                        "executable": {
                            "abs_path": "C:\\WINDOWS\\system32\\msiexec.exe", 
                            "filename": "C:\\WINDOWS\\system32\\msiexec.exe"
                        }, 
                        "bitsize": 32, 
                        "analysis_subject_id": 3, 
                        "process_id": 1724, 
                        "arguments": "C:\\WINDOWS\\system32\\msiexec.exe"
                    }
                ]
'''
def process_interactions(processes):
    a = MalwareAction()
    ao = AssociatedObject()
    a.name = "Create Mutex"
    a.type_ = "Create"
    
    ao.properties = WinProcess()
    

'''
                "mutex_opens": [
                    {
                        "mutex_name": "ShimCacheMutex"
                    }
                ]
'''
def mutex_opens(mutex):
    a = MalwareAction()
    ao = AssociatedObject()
    a.name = "Open Mutex"
    a.type_ = "Open"
    
    ao.properties = WinMutex()
    ao.properties.name = mutex["mutex_name"]
    #print ao.properties.path    # print for debug
    
    a.associated_objects = AssociatedObjects()
    a.associated_objects.append(ao)
    #print a.associated_objects.to     # debug print
    return a

'''
"mutex_creates": [
                    {
                        "mutex_name": "CTF.Layouts.MutexDefaultS-1-5-21-854245398-1202660629-725345543-1003"
                    }, 
                    {
                        "mutex_name": "Global\\{BE0D1270-9C69-4088-0C5B-B82F0AB99B3D}"
                    }, 
                    {
                        "mutex_name": "CTF.TMD.MutexDefaultS-1-5-21-854245398-1202660629-725345543-1003"
                    }, 
                    {
                        "mutex_name": "SHIMLIB_LOG_MUTEX"
                    }, 
                    {
                        "mutex_name": "CTF.Compart.MutexDefaultS-1-5-21-854245398-1202660629-725345543-1003"
                    }, 
                    {
                        "mutex_name": "CTF.Asm.MutexDefaultS-1-5-21-854245398-1202660629-725345543-1003"
                    }, 
                    {
                        "mutex_name": "CTF.TimListCache.FMPDefaultS-1-5-21-854245398-1202660629-725345543-1003MUTEX.DefaultS-1-5-21-854245398-1202660629-725345543-1003"
                    }, 
                    {
                        "mutex_name": "CTF.LBES.MutexDefaultS-1-5-21-854245398-1202660629-725345543-1003"
                    }
                ]
'''
def mutex_create(mutex):
    a = MalwareAction()
    ao = AssociatedObject()
    a.name = "Create Mutex"
    a.type_ = "Create"
    
    ao.properties = WinMutex()
    ao.properties.name = mutex["mutex_name"]
    
    a.associated_objects = AssociatedObjects()
    a.associated_objects.append(ao)
    return a

'''
"dns_queries": [
                    {
                        "hostname": "offparking.ru", 
                        "results": [
                            "195.22.26.231", 
                            "195.22.26.252", 
                            "195.22.26.253", 
                            "195.22.26.254"
                        ]
                    }, 
                    {
                        "hostname": "travelmartonline.net", 
                        "results": [
                            "182.50.130.36"
                        ]
                    }, 
                    {
                        "hostname": "finley.su"
                    }, 
                    {
                        "hostname": "update.microsoft.com", 
                        "results": [
                            "65.54.51.250"
                        ]
                    }, 
                    {
                        "hostname": "eriksiversen.ru", 
                        "results": [
                            "31.135.150.10", 
                            "62.33.95.247", 
                            "188.26.120.193", 
                            "94.244.41.195", 
                            "46.250.93.196", 
                            "178.186.212.25", 
                            "78.62.94.153", 
                            "195.90.130.19", 
                            "83.242.229.18", 
                            "94.41.55.253"
                        ]
                    }
                ]
'''
def dns_queries(dnsqueries):
    a = MalwareAction()
    ao = AssociatedObject()
    a.name = "Query DNS"
    a.type_ = "Query"
    
    # hostnameの解決
    quri = URI()
    quri.value = dnsqueries["hostname"]
    dns_question = DNSQuestion()
    dns_question.qname = quri
    ao.properties = DNSQuery()
    ao.properties.question = dns_question
    
    # resultの解決
    if dnsqueries.has_key("results"):
        records = []
        for result in dnsqueries["results"]:
            dnsrecord = DNSRecord()
            dnsrecord.domain_name = quri.value
            address = Address()
            address.CAT_IPV4
            address.address_value = result
            dnsrecord.ip_address = address
            records.append(dnsrecord)
        ao.properties.answer_resource_records = DNSResourceRecords(records)
    #print ao.properties.path    # print for debug
    
    a.associated_objects = AssociatedObjects()
    a.associated_objects.append(ao)
    #print a.associated_objects.to     # debug print
    return a

''' 要検討（TypeError: 'HTTPRequestResponse' object is not iterable）→iterable（リスト化）すればOK
"http_conversations": [
                    {
                        "src_port": 1055,                             # リクエスト
                        "response_headers": {                         #レスポンスヘッダ
                            "Transfer-Encoding": "chunked", 
                            "Content-Type": "text/html", 
                            "Status-Line": "HTTP/1.1 200 OK", 
                            "Server": "nginx", 
                            "Connection": "close", 
                            "Date": "Mon, 20 Jan 2014 10:12:27 GMT", 
                            "type": "HTTP Response"
                        }, 
                        "url": "POST /new2/gate.php HTTP/1.1",       # リクエスト行
                        "download_content": "0\r\n\r\n",             # レスポンスメッセージボディ
                        "src_ip": "192.168.0.2",                     # リクエストホストIP
                        "dst_host": "offparking.ru",                 # リクエストホスト
                        "dst_port": 80,                              # リクエストホストポート
                        "dst_ip": "195.22.26.252",                   # リクエスト
                        "protocol": "TCP", 
                        "type": "outgoing"
                    }
                     ]
'''
def http_conversations(httpconv):
    a = MalwareAction()
    ao = AssociatedObject()
    a.name = "Connect to URL"
    a.type_ = "Connect"
    
    ao.properties = NetworkConnection()
    ao.properties.layer4_protocol = httpconv["protocol"]
    
    
    header = HTTPResponseHeader()
    headerfiled = HTTPResponseHeaderFields()
    response = HTTPServerResponse()
    if httpconv["response_headers"].has_key("Transfer-Encoding"):
        headerfiled.transfer_encoding = httpconv["response_headers"]["Transfer-Encoding"]
    headerfiled.content_type = httpconv["response_headers"]["Content-Type"]
    headerfiled.server = httpconv["response_headers"]["Server"]
    headerfiled.connection = httpconv["response_headers"]["Connection"]
    #headerfiled.date = DateTime(httpconv["response_headers"]["Date"])
    t = datetime.strptime(httpconv["response_headers"]["Date"],'%a, %d %b %Y %H:%M:%S %Z').replace(tzinfo=pytz.utc)
    #print t
    headerfiled.date = DateTime(t)
    headerfiled.content_type = httpconv["response_headers"]["type"]
    header.parsed_header = headerfiled
    if httpconv.has_key("download_content"):
        body = HTTPMessage()
        body.message_body = str(httpconv["download_content"]).encode('string-escape')
        response.http_message_body = body
    
    line = HTTPStatusLine()
    tmp = httpconv["response_headers"]["Status-Line"].split()
    line.version = tmp[0]
    line.status_code = PositiveInteger(tmp[1])
    line.reason_phrase = tmp[2]
    response.http_status_line = line
    response.http_response_header = header
    
    
    client = HTTPClientRequest()
    line = HTTPRequestLine()
    tmp = httpconv["url"].split()
    line.http_method = tmp[0]
    line.value = tmp[1]
    line.version = tmp[2]    
    client.http_request_line = line
    cheader = HTTPRequestHeader()
    cheaderfiled = HTTPRequestHeaderFields()
    host = HostField()
    host.domain_name = URI(httpconv["dst_host"])
    val = Port()
    val.port_value = PositiveInteger(httpconv["dst_port"])
    host.port = val
    cheaderfiled.host = host
    cheader.parsed_header = cheaderfiled
    client.http_request_header = cheader
    
    httpsession = HTTPSession()
    requestresponse = HTTPRequestResponse()
    requestresponse.http_client_request = client
    requestresponse.http_server_response = response
    httpsession.http_request_response = [requestresponse]
    layer7 = Layer7Connections()
    layer7.http_session = httpsession
    ao.properties.layer7_connections = layer7
    #print ao.properties.to_dict()
    
    a.associated_objects = AssociatedObjects()
    a.associated_objects.append(ao)
    return a


def raised_exceptions(raised):
    pass

def jread(filepath):
    f = open(filepath, 'r')
    return json.load(f)
    f.close()

def mkBehavior():
    pass

def mkActionList(subject,mkclass):  
    token= {
            "registry_reads":       registry_reads,
            "file_reads":           file_reads,
            "loaded_libraries":     loaded_libraries,
            #"process":              process_action,
            #"overview":             overview,
            "registry_deletions":   registry_deletions,
            "file_writes":          file_writes,
            #"process_interactions": process_interactions,
            #"raised_exceptions":    raised_exceptions,
            "mutex_opens":          mutex_opens,
            "dns_queries":          dns_queries,
            "mutex_creates":        mutex_create,
            "file_deletes":         file_delete,
            "modified_libraries" :  modified_libraries,
            "http_conversations" :  http_conversations            
            }
    b = Behavior()
    ba = BehavioralAction()
    bas = BehavioralActions()
    #ba.behavioral_ordering
    bas.action = ba
    b.description = subject['overview']['analysis_reason']
    bls = []
    als = []
    for k,v in subject.items():
        if token.has_key(k):
            actions = []
            for n in v:
                act = token[k](n)               # ActionListの作成
                mkclass.bundle.actions.append(act)
                actions.append(act)
                mkclass.bundle.als.append(act)
            else:                               # Bundleにまとめる
                if len(actions) == 0:
                    print "action Null:", k 
                bas.action = actions
                b.action_composition = bas
                bls.append(b)
        else:
            print "This Key is not Checked:",k
    else:
        if als is None :
            print "ActionListNone:",subject['overview']
        mkSubject.xmlwrite(ActionList(als),BehaviorList(bls))
    
if __name__ == '__main__':
    jsonData = jread("cfe629ab66a4446588a03a8c5aaede7b.json")
    fw = open('list.log','w')
    tmp = jsonData["report"]["analysis_subjects"]
    #lists = []
    actions = []
    num=1
    test = mkSubject()
    for n in tmp:
        mkActionList(n,test)
        #actions.append(http_conversations(n))
    
    #xmlwrite(ActionList(actions))

    
    
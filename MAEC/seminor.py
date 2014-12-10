# -*- coding: utf-8 -*-
# セミナーのご案内.doc実行時の振る舞いを記述．
# sample.pyを流用

# プロセス（ツリー） in maecBundle
# analysys in Package

from cybox.core import AssociatedObjects, AssociatedObject, Object, AssociationType
from cybox.common import Hash, HashList
from cybox.objects.file_object import File
from maec.bundle.bundle import Bundle
from maec.bundle.malware_action import MalwareAction
from maec.bundle.capability import Capability
from maec.package.analysis import Analysis
from maec.package.malware_subject import MalwareSubject
from maec.package.package import Package
from cybox.utils import Namespace
import maec.utils

# サンプルの名前空間に（自動ID生成用の）IDジェネレータクラスをインスタンス化
NS = Namespace("http://example.com/", "example")
maec.utils.set_id_namespace(NS)

# インスタンス化：Bundle, Package, MalwareSubject, Analysis classes
bundle = Bundle(defined_subject=False)
package = Package()
subject = MalwareSubject()
analysis = Analysis()

# Malware Instance Object Attribures内で使うためのオブジェクトを作成（マルウェアを含んだファイル？）
subject_object = Object() #オブジェクト
subject_object.properties = File() #ファイルオブジェクト
subject_object.properties.file_name = 'seminor.doc' # ファイル名（マルウェアを含んだファイル）
subject_object.properties.size_in_bytes = '154173' #ファイルサイズ
subject_object.properties.hashes = HashList() #ファイル
subject_object.properties.hashes.append(Hash("54CC941747FA99A3521314B9969D4964"))

# 辞書から構築されたオブジェクトとマルウェアインスタンスオブジェクト属性を設定
subject.set_malware_instance_object_attributes(subject_object)
'''
# Actionで使うための関連オブジェクトのディクショナリーを作成
associated_object = AssociatedObject()
associated_object.properties = File()
associated_object.properties.file_name = 'SenpEn.exe'
associated_object.properties.file_path = r'C:\Document and settings\user\application data\Common Files\SenpEn.exe'
associated_object.properties.size_in_bytes = '8192'
associated_object.association_type = AssociationType()
associated_object.association_type.value = 'output'
associated_object.association_type.xsi_type = 'maecVocabs:ActionObjectAssociationTypeVocab-1.0'
'''

def associated(name,path,byte,value="output"):
  associated_object = AssociatedObject()
  associated_object.properties = File()
  associated_object.properties.file_name = name
  associated_object.properties.file_path = path
  associated_object.properties.size_in_bytes = byte
  associated_object.association_type = AssociationType()
  associated_object.association_type.value = value
  associated_object.association_type.xsi_type = 'maecVocabs:ActionObjectAssociationTypeVocab-1.0'

associated_t = associated("SenpEn.exe",r'C:\Document and settings\user\application data\Common Files\SenpEn.exe','8192')

associated_t = associated("word.exe",r'C:\Document and settings\user\application data\Common Files\SenpEn.exe','8192')
associated_t = associated("wcntfy.exe",r'C:\Document and settings\user\application data\Common Files\SenpEn.exe','8192')
associated_t = associated("svchost.exe",r'C:\Document and settings\user\application data\Common Files\SenpEn.exe','8192')
associated_t = associated("IEXPLORE.exe",r'C:\Document and settings\user\application data\Common Files\SenpEn.exe','8192')
associated_t = associated("word.exe",r'C:\Document and settings\user\application data\Common Files\SenpEn.exe','8192')

"""
# Create the Action from another dictionary
# 他のディクショナリーからActionの作成
action1 = MalwareAction()
action.name = 'create file'
action.name.xsi_type = 'maecVocabs:FileActionNameVocab-1.0'
action.action_status = "success"
action.associated_objects = AssociatedObjects()
action.associated_objects.append(associated_object)
"""

def action_create(name, status = "success"):
  action_s = MalwareAction()
  action_s.name = name
  action_s.name.xsi_type = 'maecVocabs:FileActionNameVocab-1.0'
  action_s.action_status = status
  return action_s

action_t = action_create("create file")
action_t.associated_objects = AssociatedObjects()
action_t.associated_objects.append(associated_t)

p_tree = ProcessTree()
root_p

# Add the Action to the Bundle
# バンドルへActionを追加
bundle.add_action(action_t)
bundle.add_process(p_tree)

"""
# Create the Capability from another dictionary
# 他のディクショナリーから機能を作成
capability = Capability()
capability.name = ''  #Voacaburaryから目的を選択？
# Add the Capability to the Bundle
# バンドルへ機能を追加
bundle.add_capability(capability)
"""
# Add the Bundle to the Malware Subject
# Malware Subjectへバンドルを追加
subject.add_findings_bundle(bundle)
# Add the Malware Subject to the Package
# パッケージへMalwareSubjectを追加
package.add_malware_subject(subject)
# Export the Package Bindings Object to an XML file and use the namespaceparser for writing out the namespace definitions
package.to_xml_file('sample_maec_package.xml', {"http://example.com/":"example"})
print "Wrote to sample_maec_package.xml"

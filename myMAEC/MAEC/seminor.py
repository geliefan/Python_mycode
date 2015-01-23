# -*- coding: utf-8 -*-
# セミナーのご案内.doc実行時の振る舞いを記述．
# sample.pyを流用

# プロセス（ツリー） in maecBundle
# analysys in Package

from cybox.core import AssociatedObjects, AssociatedObject, Object, AssociationType
from cybox.common import Hash, HashList
from cybox.objects.file_object import File
from cybox.utils import Namespace
import maec.utils
from maec.package.package import Package
from maec.package.malware_subject import MalwareSubject
from maec.package.analysis import Analysis
from maec.bundle.bundle import Bundle
from maec.bundle.malware_action import MalwareAction
from maec.bundle.process_tree import ProcessTree, ProcessTreeNode
from cybox.objects.win_executable_file_object import WinExecutableFile
from cybox.common import ToolInformation, VocabString

# サンプルの名前空間に（自動ID生成用の）IDジェネレータクラスをインスタンス化
NS = Namespace("http://example.com/", "example")
maec.utils.set_id_namespace(NS)

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
t.name = "APIMonitor"
t.vendor = "APIMonitor"
analysis.add_tool(t)

# Malware Instance Object Attribures内で使うためのオブジェクトを作成（マルウェアを含んだファイル？）
subject_object = Object() #オブジェクト
subject_object.properties = File() #ファイルオブジェクト
subject_object.properties.file_name = 'seminor.doc' # ファイル名（マルウェアを含んだファイル）
subject_object.properties.size_in_bytes = '154173' #ファイルサイズ
subject_object.properties.add_hash("54CC941747FA99A3521314B9969D4964")

# 辞書から構築されたオブジェクトとマルウェアインスタンスオブジェクト属性を設定
subject.set_malware_instance_object_attributes(subject_object)

# Actionで使うための関連オブジェクトのディクショナリーを作成
def associated(name,path,byte,value="output"):
  associated_object = AssociatedObject()
  associated_object.properties = File()
  associated_object.properties.file_name = name
  associated_object.properties.file_path = path
  associated_object.properties.size_in_bytes = byte
  associated_object.association_type = VocabString() #これはなんだ？
  associated_object.association_type.value = value
  associated_object.association_type.xsi_type = 'maecVocabs:ActionObjectAssociationTypeVocab-1.0'
  return associated_object

associated_t1 = associated("SenpEn.exe",r'C:\Document and settings\user\application data\Common Files\SenpEn.exe','3768')
associated_t2 = associated("word.exe",r'C:\Program Files\Microsoft Office\Office12\WINWORD.EXE','3408')
associated_t3 = associated("wcntfy.exe",r'C:\Documents and Settings\user\wcntfy.exe','628')
associated_t4 = associated("svchost.exe",r'C:\DOCUME~1\user\LOCALS~1\Temp\svchost.exe','2224')
associated_t5 = associated("IEXPLORE.exe",r'C:\Program Files\Internet Explorer\IEXPLORE.EXE','3764')
associated_t6 = associated("IEXPLORE.exe",r'C:\Program Files\Internet Explorer\IEXPLORE.EXE','3068')
associated_t7 = associated("word.exe",r'C:\Program Files\Microsoft Office\Office12\WINWORD.EXE','400')
aolist = [associated_t1,associated_t2,associated_t3,associated_t4,associated_t5]


# Create the create file action initiated by the root process
act1 = MalwareAction()
act1.name = "create file"
act1.name.xsi_type = "FileActionNameVocab-1.1"
act1.associated_objects = AssociatedObjects()
act1.associated_objects.append(associated_t1)


"""
プロセスツリーの作成
word
└SenPen.exe
└
"""
#Create the root Process
p_node = ProcessTreeNode()
p_node.add_initiated_action(act1.id_)
p_node.pid = 3408
p_node.name = "word.exe"

#プロセスの設定
P2 = ProcessTreeNode()
P2.pid = 3768
P2.parent_pid = 3408
P2.name = "SenPen.exe"

p_node.add_spawned_process(P2)

#ProcessTreeの設定
p_tree = ProcessTree()
p_tree.set_root_process(p_node)
#Check
#p_tree.to_xml_file('ProcessTree.xml', {"http://LIFT-S.com/":"LIFT-S"})

# パッケージへMalwareSubjectを追加
package.add_malware_subject(subject)
# バンドルへActionを追加
bundle.add_action(act1)
bundle.set_process_tree(p_tree)
# Add the Bundle to the Malware Subject
# Malware Subjectへバンドルを追加
subject.add_findings_bundle(bundle)
subject.add_analysis(analysis)

# Export the Package Bindings Object to an XML file and use the namespaceparser for writing out the namespace definitions
package.to_xml_file('MalAnalyze_seminor.xml', {"http://LIFT-S.com/":"LIFT-S"})
print "Wrote to sample_maec_package.xml"

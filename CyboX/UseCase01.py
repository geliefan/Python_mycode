# -*- coding: utf-8 -*-
import sys
import cybox.bindings.cybox_core as cybox_core_binding
from cybox.core import Observable, Observables, action, AssociatedObject, action_reference,event,object
import cybox.utils
#file:FileObject
from cybox.objects.file_object import File,FilePath
#domain:domain_nameObject
from cybox.objects.domain_name_object import DomainName
#code:CodeObject 未実装？
from cybox.objects.code_object import Code
from cybox.objects.code_object import Code

def main():
    NS = cybox.utils.Namespace("http://example.com/","example")
    cybox.utils.set_id_namespace(NS)

    """
改ざんされたサイトを特定の環境で閲覧すると「IE」がクラッシュし、
その背後でコードが実行され、
情報漏洩の原因となるマルウェアに感染する

    """
    OB = Observables()
    '''
    オブジェクトの記述
    '''
    #オブジェクト：IE(自動化したいｐ)
    IE = File()
    IE.file_name = "iexplore.exe"
    IE.file_path = r"C:\Program Files\Internet Explorer"
    IE.file_extenstion = '.exe'

    '''
    #オブジェクト：コード ＊未実装のため表記できず
    code = Code()
    code.desctiption = "攻撃コード"
    code.language = "JavaScript"
    '''
    #サイトドメイン
    domain = DomainName()
    domain.value  = "hogehoge.ccom"
    domain.type = "FQDN"

    #マルウェアファイル
    Mal = File()
    Mal.file_name = 'malware.exe'
    Mal.file_extenstion = '.exe'

    #参照関係
    ie_ao = action.AssociatedObject(IE)
    Mal_ao = action.AssociatedObject(Mal)

    #code_ao = AssociatedObject(code)
    aos1 = action.AssociatedObjects([ie_ao])
    aos2 = action.AssociatedObjects([Mal_ao])

    '''
    アクションの記述
    '''
    #閲覧
    a = action.Action()
    a.type_ = "Connect"
    a.name = "Connnect to URL"
    a.desctiption = "IE connect domain site"
    a.associated_objects = aos1
    #実行
    ae = action.Action()
    ae.type_ = "Execute"
    ae.desctiption = "Execute malware code"
    ae.associated_objects = aos2


    #アクションをイベントにセット
    aa = action.Actions([a,ae])
    e = event.Event()
    e.description = u"IEの表示とコードの実行"
    e.actions = aa

    #Observableにセット
    o1 = Observable(IE)
    o1.description = u"インターネットエクスプローラー"
    o2 = Observable(domain)
    o2.description = u"サイトドメイン"
    o3 = Observable(Mal)
    o3.description = u"マルウェアファイル"
    act = Observable(e)
    ls = [o1,o2,o3,act]
    for ob in ls:
        OB.add(ob)
    xml = open("usecase01.xml","w")
    xml.write(OB.to_xml())
    xml.close()
    print OB.to_xml()

if __name__=='__main__':
    main()

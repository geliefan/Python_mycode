# -*- coding: cp932 -*-
"""Creates the CybOX content for CybOX_Simple_Email_Pattern.xml
"""

from cybox.core import Observables
from cybox.objects.email_message_object import EmailMessage
import cybox.utils


def main():
    # 名前空間作成（URI、略）
    NS = cybox.utils.Namespace("http://example.com/", "example")
    # 名前空間設定（NS）
    cybox.utils.set_id_namespace(NS)

    # オブジェクトのプロパティを作成
    m = EmailMessage()
    m.from_ = ["attacker@example.com",
               "attacker1@example.com",
               "attacker@bad.example.com"]
    # 
    m.from_.condition = "Equals"
    m.subject = "New modifications to the specification"
    m.subject.condition = "Equals"

    print Observables(m).to_xml()

if __name__ == "__main__":
    main()

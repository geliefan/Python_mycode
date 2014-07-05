# -*- coding: cp932 -*-
"""Creates the CybOX content for CybOX_Simple_Email_Pattern.xml
"""

from cybox.core import Observables
from cybox.objects.email_message_object import EmailMessage
import cybox.utils


def main():
    # ���O��ԍ쐬�iURI�A���j
    NS = cybox.utils.Namespace("http://example.com/", "example")
    # ���O��Ԑݒ�iNS�j
    cybox.utils.set_id_namespace(NS)

    # �I�u�W�F�N�g�̃v���p�e�B���쐬
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

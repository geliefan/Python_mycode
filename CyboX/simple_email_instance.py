#!/usr/bin/env python
# -*- coding: cp932 -*-

# Copyright (c) 2014, The MITRE Corporation. All rights reserved.
# See LICENSE.txt for complete terms.

"""Creates the CybOX content for CybOX_Simple_Email_Instance.xml
"""

from cybox.core import Observables
from cybox.objects.address_object import Address
from cybox.objects.email_message_object import EmailMessage
import cybox.utils


def main():
    NS = cybox.utils.Namespace("http://example.com/", "example")
    cybox.utils.set_id_namespace(NS)

    # オブジェクトの作成（EmailMesage)
    m = EmailMessage()
    # オブジェクトに関連付け
    m.to = ["victim1@target.com", "victim2@target.com"]
    m.from_ = "attacker@example.com"
    m.subject = "New modifications to the specification"

    # オブジェクトの作成（Adress)
    a = Address("192.168.1.1", Address.CAT_IPV4)

    # オブジェクト間の関連
    m.add_related(a, "Received_From", inline=False)
    a.add_related(m, "Received_to", inline=False)

    print Observables([m, a]).to_xml()

if __name__ == "__main__":
    main()

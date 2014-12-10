# -*- coding: utf-8 -*-
'''
パケット解析にdpktを使ってみる
dpkt:https://code.google.com/p/dpkt/
参考：http://isiz.hateblo.jp/entry/2013/10/31/Python%E3%81%A7%E3%83%91%E3%82%B1%E3%83%83%E3%83%88%E8%A7%A3%E6%9E%90%EF%BC%88dpkt%EF%BC%89_%E3%81%9D%E3%81%AE%EF%BC%91%EF%BD%9E%E7%B0%A1%E5%8D%98%E3%81%AA%E8%AA%AD%E3%81%BF%E8%BE%BC%E3%81%BF%EF%BD%9E
三村ツールができるまでの間のつなぎとして
'''
from __future__ import unicode_literals
from __future__ import with_statement

import dpkt,socket

#pcapファイル
file = r"C:\WORK\GitHub\Python_mycode\CyboX\seccon2014.pcap"

with open(file, "rb") as f:
    pcr = dpkt.pcap.Reader(f)
    count = 0
    for ts, buf in pcr:
        count += 1
        print "Packet %d:%d" % (count, ts)
        try:
            eth = dpkt.ethernet.Ethernet(buf)
        except:
            print "Error: Packet No.%d" % count
        #IPパケットかの判定
        if type(eth.data) == dpkt.ip.IP:
            ip = eth.data
            print "", "IP: %s -> %s" % (socket.inet_ntoa(ip.src), socket.inet_ntoa(ip.dst))

            #TCPパケットかの判定
            if type(ip.data) == dpkt.tcp.TCP:
                tcp = ip.data
                print "","", "Port: %d -> %d" % (tcp.sport, tcp.dport)

                #HTTP Requestかの判定
                if tcp.dport == 80 and len(tcp.data) > 0:
                    httpreq = dpkt.http.Request(tcp.data)
                    print "", "", "Rquest:", httpreq.headers


                #HTTP Responseかの判定
                if tcp.sport == 80 and len(tcp.data) > 0 and (dpkt.ip.IP_DF & ip.off) == 0:
                    httpres = dpkt.http.Response(tcp.data)
                    print "", "", "Response:", httpres.headers

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Demo script sending a simple text/plain message with mailutil module
"""

# from standard lib
import sys
import os
import socket
import pprint
import time
import ssl
import email.mime.text

# from PySocks
import socks

# the mail utility module
import mailutil

# prepare SOCKS proxy usage
#SMTP_PROXY = {
#    'proxytype':socks.PROXY_TYPE_SOCKS5,
#    'addr':'socks-proxy.example.com',
#    'port':1080,
#    'rdns':True,
#    'username':None,
#    'password':None,
#}

# don't use proxy here
SMTP_PROXY = None

SMTP_LOCALHOSTNAME = 'myhost.example.com'

# example for using SMTPS
SMTP_URL = 'smtps://smtp.example.com/?VIA=srv1.example.com'
# example for using SMTP with STARTTLS
#SMTP_URL = 'smtp://smtp.example.com/?STARTTLS&VIA=10.20.30.40'

SMTP_TLSARGS = {
    'cert_reqs':ssl.CERT_OPTIONAL,
    'ssl_version':ssl.PROTOCOL_TLSv1,
    'ca_certs':'/etc/ssl/ca-bundle.pem',
    # cert-pinning
    'expected_fingerprints':None,
    # for using TLS client cert
    #'keyfile':None,
    #'certfile':None,
    # set acceptable TLS ciphers
    #'ciphers':None,
}


# Build e-mail message object
headers = (
    ('From', u'Michael Ströder <michael@stroeder.com>'),
    ('To', u'Michael Ströder <michael@stroeder.com>'),
    ('Subject', u'test subject äöüÄÖÜß'),
    ('Date', time.strftime('%a, %d %b %Y %T %z', time.gmtime(time.time()))),
)
msg = u'äöüÄÖÜß'

# OpenSMTP connection and send mail

if SMTP_PROXY != None:
    # set socket class to be used by mailutil to PySocks implementation
    import socks
    mailutil.smtp_socket = socks.socksocket
    socks.setdefaultproxy(**SMTP_PROXY)
else:
    # use socket class from standard lib
    mailutil.smtp_socket = socket.socket

smtp_conn = mailutil.smtp_connection(
    SMTP_URL,
    local_hostname=SMTP_LOCALHOSTNAME,
    tls_args=SMTP_TLSARGS,
    debug_level=9
)
smtp_conn.send_simple_message(
    'michael@stroeder.com',
    ['michael@stroeder.com'],
    'utf-8',
    headers,
    msg,
)
smtp_conn.quit()

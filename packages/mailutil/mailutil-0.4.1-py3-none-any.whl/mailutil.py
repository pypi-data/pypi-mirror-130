# -*- coding: utf-8 -*-
"""
Helper module for using smtplib for secured connections

Author: Michael Ströder <michael@stroeder.com>

mainly a wrapper around smtplib.SMTP etc.
"""

__version__ = '0.4.1'

import socket
import smtplib
import email
import email.mime.text
import ssl
import urllib.parse

urllib.parse.uses_query.extend(['smtp', 'smtps'])

SMTP_SOCKET = socket.socket

#-----------------------------------------------------------------------
# Classes and functions
#-----------------------------------------------------------------------


class SMTPHelper:
    """
    Mix-in class with convenience methods
    """

    def send_simple_message(
            self,
            from_addr,
            to_addr,
            charset,
            headers,
            msg
        ):
        """
        Send a simple text/plain message
        """
        e_mail = email.mime.text.MIMEText(msg, 'plain', charset)
        e_mail.set_charset(charset)
        for header_name, header_value in headers:
            e_mail[header_name] = header_value
        self.sendmail(from_addr, to_addr, e_mail.as_string())
        # end of send_simple_message()


class SMTP(smtplib.SMTP, SMTPHelper):
    """
    SMTP connection class
    """


class SMTP_SSL(smtplib.SMTP_SSL, SMTPHelper):
    """
    SMTPS connection class
    """


def smtp_connection(
        smtp_url,
        local_hostname=None,
        ca_certs=None,
        timeout=60,
        debug_level=0
    ):
    """
    This function opens a SMTP connection specified by `smtp_url'.

    It also invokes `SMTP.starttls()' or `SMTP.login()' if URL contains
    appropriate parameters.
    """

    def smtp_tls_context(ca_certs):
        ctx = ssl.SSLContext()
        ctx.verify_mode = ssl.CERT_REQUIRED
        ctx.check_hostname = True
        ctx.load_verify_locations(ca_certs, capath=None, cadata=None)
        return ctx

    smtp_url_obj = urllib.parse.urlparse(smtp_url)
    query_obj = urllib.parse.parse_qs(
        smtp_url_obj.query,
        keep_blank_values=True,
        strict_parsing=False
    )
    if smtp_url_obj.scheme == 'smtp':
        # Start clear-text connection
        smtp_conn = SMTP(
            host=smtp_url_obj.hostname,
            port=smtp_url_obj.port,
            local_hostname=local_hostname,
            timeout=timeout,
        )
        # Check whether STARTTLS was provided in URL
        if 'STARTTLS' in query_obj:
            smtp_conn.starttls(
                context=smtp_tls_context(ca_certs),
            )
    elif smtp_url_obj.scheme == 'smtps':
        smtp_conn = SMTP_SSL(
            host=smtp_url_obj.hostname,
            port=smtp_url_obj.port,
            local_hostname=local_hostname,
            timeout=timeout,
            context=smtp_tls_context(ca_certs),
        )
    else:
        raise ValueError('Unsupported URL scheme %r' % (smtp_url_obj.scheme))
    # Login if username and password were provided in URL
    if smtp_url_obj.username and smtp_url_obj.password:
        smtp_conn.login(smtp_url_obj.username, smtp_url_obj.password)
    smtp_conn.set_debuglevel(debug_level)
    return smtp_conn
    # end of smtp_connection()

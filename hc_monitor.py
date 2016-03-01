__author__ = 'root'
# -*- coding: UTF-8 -*-
#Import modules
import smtplib
import sys
import subprocess
import socket
from email.mime.text import MIMEText

#Send mail
class MailToWarn():
    def __init__(self,mailto_list,mail_host,mail_user,mail_pass):
        self.mailto_list=mailto_list
        self.mail_host=mail_host
        self.mail_user=mail_user
        self.mail_pass=mail_pass

    def send_mail(self,content):
        msg = MIMEText(content,_subtype='html',_charset='gb2312')
        msg['Subject'] = "Hexconnect error!"    #Email subject
        msg['From'] = self.mail_user
        msg['To'] = self.mailto_list

        try:
            s = smtplib.SMTP()
            s.connect(self.mail_host)  #SMTP server
            s.login(self.mail_user,self.mail_pass)  #login
#            s.sendmail(self.mail_user, self.mailto_list, msg.as_string())  #sendmail
            s.sendmail(self.mail_user, self.mailto_list, msg.as_string())  #sendmail
            s.close()
            return True
        except Exception, e:
            print str(e)
            return False


#Detect errors

#Process monitor
#def monitor_process(key_word, cmd):
def monitor_process(key_word):
    p1 = subprocess.Popen(['ps', '-ef'], stdout=subprocess.PIPE)
    p2 = subprocess.Popen(['grep', key_word], stdin=p1.stdout, stdout=subprocess.PIPE)
    p3 = subprocess.Popen(['grep', '-v', 'grep'], stdin=p2.stdout, stdout=subprocess.PIPE)
    lines = p3.stdout.readlines()
    if len(lines) > 0:
        return True
    else:
        return False
#    sys.stderr.write('process[%s] is lost, run [%s]\n' % (key_word, cmd))
#    sys.stderr.write('Process:[%s] is lost!\n' % (key_word))
#    subprocess.call(cmd, shell=True)

#Port monitor
#def monitor_port(protocol, port, cmd):
def monitor_port(protocol, port):
    address = ('127.0.0.1', port)
    socket_type = socket.SOCK_STREAM if protocol == 'tcp' else socket.SOCK_DGRAM
    client = socket.socket(socket.AF_INET, socket_type)
    try:
        client.bind(address)
    except Exception, e:
        pass
        return True
    else:
#        sys.stderr.write('port[%s-%s] is lost, run [%s]\n' % (protocol, port, cmd))
#        subprocess.call(cmd, shell=True)
        return False
    finally:
        client.close()

#Main
if __name__ == '__main__':
    #mail content
    content = """
    Hexconnect error!
    Maybe hexconnect is offline.
    You should check it out!
    """
    #key word of hexconnect process
    key_word="hexconnect"
    #port monitor protocol and port
    protocol="tcp"
    port=9933
    if monitor_process(key_word):
        if monitor_port(protocol,port):
            print "Hexconnect is fine."
        else:
#    MailToWarn.mailto_list=sys.argv[1]
#    MailToWarn.mail_host=sys.argv[2]
#    MailToWarn.mail_user=sys.argv[3]
#    MailToWarn.mail_pass=sys.argv[4]
            SendMail=MailToWarn(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])
            if SendMail.send_mail(content):
                print "Email sent successfully!"
            else:
                print "Failed!"







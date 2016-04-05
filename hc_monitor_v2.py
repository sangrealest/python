#!/usr/bin/python

#Import modules
import sys
import subprocess
import socket
import time
#from email.mime.text import MIMEText

#define time
cur_time = time.strftime('%Y-%m-%d %X')

#define monitor
#define process monitor
def monitor_process(key_word,key_count):
    p1 = subprocess.Popen(['ps', '-ef'], stdout=subprocess.PIPE)
    p2 = subprocess.Popen(['grep', key_word], stdin=p1.stdout, stdout=subprocess.PIPE)
    p3 = subprocess.Popen(['grep', '-v', 'grep'], stdin=p2.stdout, stdout=subprocess.PIPE)
    lines = p3.stdout.readlines()
    if len(lines) == key_count:
        return 2
    elif len(lines) < key_count and len(lines) > 0:
        return 3
    elif len(lines) == 0:
        return 4
    else:
        return 6

#define port monitor
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



#config file
task_id=sys.argv[1]
host=sys.argv[2]
conf=sys.argv[3]
conf_path="/home/common/MonitorV3/scripts/"+str(conf)
file=open(conf_path).readlines()


for line in file:
    key_word=line.split('"')[1]     #The process key word
    key_count=int(line.split('"')[3])    #The process count
    protocol=line.split('"')[5]
    port=line.split('"')[7]

    if protocol=="null" or port=="null":
        status=monitor_process(key_word,key_count)
        if status==2:
            result=key_word+" is fine."
        elif status==3:
            result=key_word+" alert!"
        elif status==4:
            result=key_word+" is critical!"
        else:
            result="Unknown error!"
    else:
        status=monitor_process(key_word,key_count)
        if status==2:
            result=key_word+" is fine."
        elif status==3:
            result=key_word+" alert!"
        elif status==4:
            result=key_word+" is critical!"
        else:
            result="Unknown error!"
        if not monitor_port(protocol,int(port)):
            status=4
            result=key_word+" is critical!"
            break


print ("{" + '"result"' + ":"  + "\"" + result + "\"" + ',' + "\"status\"" + ":" + "\"" + str(status) + "\"" + ',' + "\"time\"" + ":" + "\"" + cur_time + "\""+ ',' + "\"id\"" + ":" + "\"" + task_id  + "\""+ ',' + "\"info\"" + ":"+  "\"\"" + "}")







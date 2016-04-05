#Monitor ControllerX64.exe
#Author:Shanker
import psutil
import sys
import time
import os


now = time.strftime('%Y-%m-%d %X')

taskid = sys.argv[1]

host = sys.argv[2]

conf = sys.argv[3]

path = "C:\\CGuardian\\scripts\\" + str(conf)

scriptname = sys.argv[0][sys.argv[0].rfind(os.sep)+1:]

def processinfo(processName):
    pids = psutil.pids()
    a = 1
    for pid in pids:
        p = psutil.Process(pid)
        if p.name() == processName:
            status = 2
            result = "The Game Process is running"
            a += 1
    if a == 1:
        status= 4
        result = "The Game Process is down"


    f=open("C:\\CGuardian\\scripts\\%s.1" % scriptname,'w')

    f.write("{" + '"result"' + ":"  + "\"" + result + "\"" + ',' + "\"status\"" + ":" + "\"" + str(status) + "\"" + ','\
 + "\"time\"" + ":" + "\"" + now + "\""+ ',' + "\"id\"" + ":" + "\"" + taskid  + "\""+ ',' + "\"info\"" + ":"+  "\"\"" + "}")

    f.close()


    print ("{" + '"result"' + ":"  + "\"" + result + "\"" + ',' + "\"status\"" + ":" + "\"" + str(status) + "\"" + ',' + \
        "\"time\"" + ":" + "\"" + now + "\""+ ',' + "\"id\"" + ":" + "\"" + taskid  + "\""+ ',' + "\"info\"" + ":"+  "\"\"" + "}")

processinfo("ControllerX64.exe")

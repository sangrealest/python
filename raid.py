# -*- coding: UTF-8 -*-
#import modules
import re
import os
import time
import sys
import subprocess


now = time.strftime('%Y-%m-%d %X')

taskid = sys.argv[1]

host = sys.argv[2]

conf = sys.argv[3]

dir = os.getcwd()

path = "C:\\CGuardian\\scripts\\" + str(conf)

rlpath = "C:\\CGuardian\\scripts\\" + "raid.log"

scriptname=sys.argv[0][sys.argv[0].rfind(os.sep)+1:]

#os.system("C://CGuardian//tools//Megacli.exe -PDlist -aALL>.//raid.log")

raidlog = subprocess.check_output('C://CGuardian//tools//Megacli.exe -PDlist -aALL')

rf = open(rlpath,"w")

for i in raidlog:

    rf.write(i)

rf.close()

raid_log = open(rlpath,"r")

for line in raid_log.readlines():

    err1 = re.findall('Unconfigured\(bad\)',line)

    err2 = re.findall('Failed',line)

#    err3 = re.findall('Predictive\ Failure\ Count:\ 1',line)

    warn = re.findall('YES',line)

    status = 2

    result = "Raid is fine!"

    if err1:

        status = 4

        result = "Bad drive detected!"

        break

    if err2:

        status = 4

        result = "Drive failure detected!"

        break

    # if err3:
    #
    #     status = 4
    #
    #     result = "Predictive failure detected!"
    #
    #     break

    if warn:

        status = 4

        result = "Raid SMART alert detected!"

        break

raid_log.close()

f=open("C:\\CGuardian\\scripts\\%s.1" % scriptname,'w')

f.write("{" + '"result"' + ":"  + "\"" + result + "\"" + ',' + "\"status\"" + ":" + "\"" + str(status) + "\"" + ',' + "\"time\"" + ":" + "\"" + now + "\""+ ',' + "\"id\"" + ":" + "\"" + taskid  + "\""+ ',' + "\"info\"" + ":"+  "\"\"" + "}")

f.close()

print ("{" + '"result"' + ":"  + "\"" + result + "\"" + ',' + "\"status\"" + ":" + "\"" + str(status) + "\"" + ',' + "\"time\"" + ":" + "\"" + now + "\""+ ',' + "\"id\"" + ":" + "\"" + taskid  + "\""+ ',' + "\"info\"" + ":"+  "\"\"" + "}")


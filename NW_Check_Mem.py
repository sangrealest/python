import os

import sys

import subprocess

import time

import psutil


now = time.strftime('%Y-%m-%d %X')

taskid = sys.argv[1]

host = sys.argv[2]

conf = sys.argv[3]

dir = os.getcwd()

path = "C:\\CGuardian\\scripts\\" + str(conf)

scriptname=sys.argv[0][sys.argv[0].rfind(os.sep)+1:]

file=open(path).readlines()

mem_usage = int(psutil.virtual_memory()[2])


for line in file:



        min_threshold = int(line.split('"')[1])



        max_threshold = int(line.split('"')[3])



        if mem_usage < min_threshold:

                status = 2

        elif mem_usage >= min_threshold and mem_usage < max_threshold:

                status = 3

        elif mem_usage >= max_threshold:

                status = 4

        else:

                status = 6



result = "the memory usage is " + " " + str(mem_usage) + "%"


f=open("C:\\CGuardian\\scripts\\%s.1" % scriptname,'w')


f.write("{" + '"result"' + ":"  + "\"" + result + "\"" + ',' + "\"status\"" + ":" + "\"" + str(status) + "\"" + ',' + "\"time\"" + ":" + "\"" + now + "\""+ ',' + "\"id\"" + ":" + "\"" + taskid  + "\""+ ',' + "\"info\"" + ":"+  "\"\"" + "}")


f.close()


print ("{" + '"result"' + ":"  + "\"" + result + "\"" + ',' + "\"status\"" + ":" + "\"" + str(status) + "\"" + ',' + "\"time\"" + ":" + "\"" + now + "\""+ ',' + "\"id\"" + ":" + "\"" + taskid  + "\""+ ',' + "\"info\"" + ":"+  "\"\"" + "}")



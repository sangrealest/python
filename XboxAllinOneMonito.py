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

line=open(path).readline()


min_threshold = int(line.split('"')[1])

max_threshold = int(line.split('"')[3])

i = 1


cpu_usage1 = int(psutil.cpu_percent())

disk_usage1 = int(psutil.disk_usage('/')[3])

mem_usage1 = int(psutil.virtual_memory()[2])

time.sleep( 10 )

cpu_usage2 = int(psutil.cpu_percent())

disk_usage2 = int(psutil.disk_usage('/')[3])

mem_usage2 = int(psutil.virtual_memory()[2])

cpu_usage = int((cpu_usage1 + cpu_usage2)/2)

mem_usage = int((mem_usage1 + mem_usage2)/2)

disk_usage = int((disk_usage1 + disk_usage2)/2)


for i in range(1,4):

        if cpu_usage < min_threshold:

                status_cpu = 2

        elif cpu_usage >= min_threshold and cpu_usage < max_threshold:

                status_cpu = 3

        elif cpu_usage >= max_threshold:

                status_cpu = 4
        else:
                status_cpu = 6

        if mem_usage < min_threshold:

                status_mem = 2

        elif mem_usage >= min_threshold and mem_usage < max_threshold:

                status_mem = 3

        elif mem_usage >= max_threshold:

                status_mem = 4

        else:

                status_mem = 6

        if disk_usage < min_threshold:

                status_disk = 2

        elif disk_usage >= min_threshold and disk_usage < max_threshold:

                status_disk = 3

        elif disk_usage >= max_threshold:

                status_disk = 4

        else:

                status_disk = 6

        if cmp(status_cpu, status_mem) == 1:

                if cmp(status_cpu, status_disk) == 1:

                        status = status_cpu

                elif cmp(status_mem, status_disk) == 1:

                        status = status_mem
                else:
                        status = status_disk

        elif cmp(status_cpu, status_disk) == 1:

                status = status_mem

        elif cmp(status_mem,status_disk) == 1:

                status = status_mem
        else:
                status = status_disk

        i = i + 1


result = "the cpu, mem, disk usage is " + " " + str(cpu_usage) + "%," + str(mem_usage) + "%," + str(disk_usage) + "%"


f=open("C:\\CGuardian\\scripts\\%s.1" % scriptname,'w')

f.write("{" + '"result"' + ":"  + "\"" + result + "\"" + ',' + "\"status\"" + ":" + "\"" + str(status) + "\"" + ','\
 + "\"time\"" + ":" + "\"" + now + "\""+ ',' + "\"id\"" + ":" + "\"" + taskid  + "\""+ ',' + "\"info\"" + ":"+  "\"\"" + "}")

f.close()


print ("{" + '"result"' + ":"  + "\"" + result + "\"" + ',' + "\"status\"" + ":" + "\"" + str(status) + "\"" + ',' + \
        "\"time\"" + ":" + "\"" + now + "\""+ ',' + "\"id\"" + ":" + "\"" + taskid  + "\""+ ',' + "\"info\"" + ":"+  "\"\"" + "}")

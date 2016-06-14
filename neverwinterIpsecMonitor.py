import sys

import wmi

import subprocess

import time

import os

import re



c = wmi.WMI()

now = time.strftime('%Y-%m-%d %X')

taskid = sys.argv[1]

host = sys.argv[2]

conf = sys.argv[3]

path = "C:\\CGuardian\\scripts\\" + str(conf)

scriptname = sys.argv[0][sys.argv[0].rfind(os.sep)+1:]

file=open(path).readlines()

d = {}

r = []

rule_status = []

rule_result = []

filter_status = []

filter_result = []

rule_count_status = []

rule_count_result = []

sys_filter_status = []

sys_filter_result = []



##Init system environment##



sys_policy = subprocess.check_output('netsh ipsec static show policy all')

sys_rule = subprocess.check_output('netsh ipsec static show policy wudong level = Verbose Format = table')

sys_rule_name = subprocess.check_output("netsh ipsec static show rule all policy = wudong level = Verbose Format = table | find \"Rule Name\" | find /v \"NONE\"",shell=True)

sys_verbose_unformat = subprocess.check_output("netsh ipsec static show rule all policy = wudong level = Verbose Format = table")

blank=re.compile('\s+') 

sys_verbose=re.sub(blank,'',sys_verbose_unformat)

del_enter = re.sub(r'\r\n255','255',sys_verbose_unformat)

tmp_file=open("C:\\CGuardian\\scripts\\%s.log" % scriptname,'w')

tmp_file.write('%s' %del_enter)

tmp_file.close()

correct_ipsec = open("C:\\CGuardian\\scripts\\%s.log" % scriptname)

sys_ipsec = open("C:\\CGuardian\\scripts\\tfile.log",'w')

t = open("C:\\CGuardian\\scripts\\tfile.log",'a')

t.truncate()

t.close()



for line in file:

        servername =line.split('"')[1]

        conf_policyname =line.split('"')[3]

        conf_rulenum = line.split('"')[5]

        conf_rulename =line.split('"')[7]

        conf_filternum = line.split('"')[9]

        conf_filter = line.split('"')[11]



##Init rule total and filter total ##



        rule_total = 0

        filter_total = 0               

            

##Check if policy name in conf is correct##



        name = re.findall('%s' % conf_policyname,sys_policy)

        if name:

                status = 2

                result= ""

        else:

                status = 4

                result = "IPSec policy name error!!!"

        d["policy_correct_status"] = status

        d["policy_correct_result"] = str('%s' %result)



##Check if policy was assigned##



        assign = re.findall('YES',sys_policy)

        if assign:

                status = 2

                result = ""

        else:

                status = 4

                result = "IPSec policy not assigned!!!"

        d["policy_assign_status"] = status

        d["policy_assign_result"] = str('%s' %result)



##Check rule count,and subtract the default rule "Dynamic" which is empty ##



        rule_name = re.findall ('Rule Name',sys_verbose_unformat)

        for name in rule_name:

                num = name.split(',')

                rule_total += int(num.count('%s' % name))

                total = rule_total - 1

        if int(conf_rulenum) == int(total):

                status = 2

                rule_count_status.append(status)

                

        else:

                status = 4

                result = "IPSec rule number err!!!"

                rule_count_status.append(status)

                rule_count_result.append(result)

        d["rule_count_status"] = max(rule_count_status)

        rule_count_tmp = re.findall('IPSec rule number err!!!','%s' % rule_count_result)

        if rule_count_tmp:

                d["rule_count_result"] = "IPSec rule number err!!!"

        else:

                d["rule_count_result"] = ""



##Check if rule in conf was assigned##



        assign = re.findall ('%s' % conf_rulename,sys_rule_name)

        if assign:

                status = 2

                result = ""

                rule_status.append(status)

        else:

                status = 4

                result = "IPSec rule name err!!!"

                rule_status.append(status)

                rule_result.append(result)

        d["rule_assign_status"] = max(rule_status)

        rule_result_tmp = re.findall('IPSec rule name err!!!','%s' % rule_result)

        if rule_result_tmp:

                d["rule_assign_result"] = "IPSec rule name err!!!"

        else:

                d["rule_assign_result"] = ""

                    

##Check if filter in conf was assigned##

        for format in correct_ipsec:

                change = re.sub(r'\s','',format)

                YES = re.findall('^YES.*',change)

                if YES:

                        t = open("C:\\CGuardian\\scripts\\tfile.log",'a')

                        t.write('%s' %YES + '\n')

                        t.close()

        filter = re.findall('%s' % conf_filter,open('C:\\CGuardian\\scripts\\tfile.log', 'r').read())

        if filter:

                status = 2

                result = ""

                filter_status.append (status)

                filter_result.append (result)

        else:

                status = 4

                print conf_filter

                result = "IPSec filter in system err!!!"

                filter_status.append (status)

                filter_result.append (result)

        d["filter_status"] = max(filter_status)

        f = re.findall('IPSec filter in system err!!!','%s' % filter_result)

        if f:

                d["filter_result"] = "IPSec filter in system err!!!"

        else:

                d["filter_result"] = ""



##Check if sys filter was configed in file##

        for sys_filter in sys_ipsec:

                change = re.sub(r'\'','',sys_filter)

                change1 = re.sub(r'\[','',change)

                change2 = re.sub(r'\]','',change1)

                change3 = re.sub(r'\s','',change2)

                a = re.findall('%s' % change3,open(path,'r').read())

                if a:

                        status = 2

                        result = ""

                        sys_filter_status.append (status)

                        sys_filter_result.append (result)

                else:

                        status = 4

                        print change3

                        result = "IPSec filter in conf err!!!"

                        sys_filter_status.append(status)

                        sys_filter_result.append(result)

                d["sys_filter_status"] = max(sys_filter_status)

                f = re.findall('IPSec filter in conf err!!!','%s' % sys_filter_result)

                if f:

                        d["sys_filter_result"] = "IPSec filter in conf err!!!"

                else:

                        d["sys_filter_result"] = ""



r.append(d)

d = {}



    

##status = 0

result = ""

for line in r:

       res = "%s%s%s%s%s%s" % (line["policy_correct_result"],line["policy_assign_result"],line["rule_count_result"],line["rule_assign_result"],line["filter_result"],line["sys_filter_result"])

##        res += "%"

##       if line["status"] > status:

##                status = line["status"]

       status = []

       status.append (line["policy_correct_status"])

       status.append (line["policy_assign_status"])

       status.append (line["rule_count_status"])

       status.append (line["rule_assign_status"])

       status.append (line["filter_status"])

       status.append (line["sys_filter_status"])

       status = max(status)

       result = result + " " + res



f=open("C:\\CGuardian\\scripts\\%s.1" % scriptname,'w')

f.write("{" + '"result"' + ":"  + "\"" + result + "\"" + ',' + "\"status\"" + ":" + "\"" + str(status) + "\"" + ',' + "\"time\"" + ":" + "\"" + now + "\""+ ',' + "\"id\"" + ":" + "\"" + taskid  + "\""+ ',' + "\"info\"" + ":"+  "\"\"" + "}")

f.close()



##print ("{" + '"result"' + ":"  + "\"" + result + "\"" + ',' + "\"status\"" + ":" + "\"" + str(status) + "\"" + ',' + "\"time\"" + ":" + "\"" + now + "\""+ ',' + "\"id\"" + ":" + "\"" + taskid  + "\""+ ',' + "\"info\"" + ":"+  "\"\"" + "}")

print ("{" + '"result"' + ":"  + "\"" + result + "\"" + ',' + "\"status\"" + ":" + "\"" + str(status) + "\"" + ',' + "\"time\"" + ":" + "\"" + now + "\""+ ',' + "\"id\"" + ":" + "\"" + taskid  + "\""+ ',' + "\"info\"" + ":"+  "\"\"" + "}")


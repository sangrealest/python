#!/usr/bin/python
import sys
import os
import poplib
import base64
import time
def openFile(filePath):
    myFile = open(filePath)
    myContent = myFile.readlines()
    tmpList = []
    for i in myContent:
        i = i.strip()
        j = i.split("=")
        tmpList.append(j[1])
    return tmpList
    
def getSubList(mailObj,mailNums):
    subjectList = []
    subjectId = []
    for i in range(mailstart,mailNums+1):
        dlMail = mailObj.retr(i)
        for j in dlMail[1]:
            if j.find("Subject:") != -1 and (j.find("is down!") != -1 or j.find("is up!") != -1) and j.find("NeverwinterCNXboxOne") == -1 and j.find("China_HKX_Analytics") == -1 and j.find("China_Xbox_Analytics") == -1 and j.find("Xbox") == -1:
                subjectList.append(j)
                subjectId.append(i)
    print subjectList 
    return (subjectList,subjectId)

def groupBySub(subjectList):
    groupBy = []
    groupByTmp = []
    for i in subjectList:
        tmpList = i.split(' ')
        mark = 0
        for sid in groupByTmp:
            if tmpList[1] == sid:
                mark +=1
                break
        groupByTmp.append(tmpList[1])
        if mark == 0:
            groupBy.append(tmpList[1])
    return groupBy
#base info
if len(sys.argv) != 4:
    print "input error!retry pls!"
    sys.exit(0)
id = sys.argv[1]
null1 = sys.argv[2]
null2 =sys.argv[3]
status = 2
info = "\n"
timeStamp = int(time.time())
timeArray = time.localtime(timeStamp)
checkTime = time.strftime("%Y-%m-%d %H:%M", timeArray)


filePath = "./login.conf"
infoList = openFile(filePath)
userName = infoList[0]
passwd = infoList[1]
host = infoList[2]

mailObj = poplib.POP3(host)
mailObj.set_debuglevel(0)
mailObj.user(userName)
mailObj.pass_(passwd)

statResult = mailObj.stat()
mailNums = statResult[0]
if mailNums > 500:
    mailstart = mailNums - 500
else:
    mailstart = 1
mailCount = statResult[1]
#print mailNums

#groupBy for subject
tupleTmp = getSubList(mailObj,mailNums)
subjectList = tupleTmp[0]
subjectId = tupleTmp[1]
groupBy = groupBySub(subjectList)


#mk activeVar
subGroup = {}
subIdGroup = {}
for i in groupBy:
    subGroup[i] = []
    subIdGroup[i] = []   


for a,i in enumerate(subjectList):
    tmpList = i.split(' ')
    for j in groupBy:
        if tmpList[1] == j:
            subGroup[j].append(i)
            subIdGroup[j].append(subjectId[a])


for i in subGroup.keys():
    if subGroup[i][-1].find("is down!") != -1:
        status = 4
        info = "%s%s\n" %(info,subGroup[i][-1])
        #print info
    else:
        for j in subIdGroup[i]:
            os.system("echo '%s DEL' >> /tmp/mailDownUpDel.log" %subGroup[i][-1])
            mailObj.dele(j)

if status == 4:
    dest = os.popen("/bin/echo '%s' |/bin/gzip -9" %info)
    info = base64.b64encode(dest.read())
    print "{\"result\":\"[warning]\",\"status\":\"4\",\"time\":\"%s\",\"id\":\"%s\",\"info\":\"%s\"}" %(checkTime,id,info)

else:
    print "{\"result\":\"[normal]\",\"status\":\"2\",\"time\":\"%s\",\"id\":\"%s\",\"info\":\"\"}" %(checkTime,id)

mailObj.quit()

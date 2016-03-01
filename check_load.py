#!/usr/bin/python
import os,sys,base64,time,re,commands

def option():
    try:
        config = {'id':sys.argv[1],'server':sys.argv[2],'file':sys.argv[3]}
    except:
        sys.exit(2)
    return config

if __name__ == '__main__':
    opt = option()
    try:
        id = opt['id']
        configfile = opt['file']
        server = opt['server']
    except Exception,e:
        print 'config error:' + str(e)
        sys.exit(2)
    
#    param_list = ['sel','list']

    try:
        configs = open(configfile,'r')
        config_list = []
        config = {}
        for conf in configs.readlines():
            temp = conf.strip('\n').split(',')
            for i in temp:
                config[i.split('=')[0]] = i.split('=')[1]
            config_list.append(config)
            config = {}
        configs.close()
    except Exception,e:
        print 'error:' + str(e)
        sys.exit(2)
    
    allow_list = []
    flag = False

    if server == 'localhost' or server == 'manager':
        result = {}
        res = ''
#        for i in config_list:
#            flag = 0
#            for j in i['param'].split(' '):
#                for k in param_list:
#                    if k == j:
#			flag = flag + 1
#                        break
#            if flag == len(i['param'].split(' ')):
        for i in config_list:
            if re.search(r'\"',str(i['key'])) or re.search(r'\|',str(i['key'])) or re.search(r'\'',str(i['key'])) or re.search(r'&',str(i['key'])):
                result['result'] = 'key error'
                result['status'] = '4'
                result['id'] = id
                result['time'] = time.strftime('%Y-%m-%d %H:%M',time.localtime(time.time()))
                result['info'] = base64.encodestring(i['key']).replace("\n","")
                print str(result).replace("\'","\"")
                sys.exit(0)
            else:
                allow_list.append(i)
        for i in allow_list:
#            try:
#                pf = open(i['password'],'r')
#                pwd = pf.readline().strip('\n')
#                #param = i['param']
#                param = "sel list"
#                key = i['key']
#                pf.close()
#            except Exception,e:
#                print 'error' + str(e)
#                sys.exit(2)
            try:
                logtime = time.strftime('%Y-%m-%d',time.localtime(time.time()))
                cmd = "sudo /usr/bin/uptime 2>/dev/null |grep load | awk -F'average:' '{print $2}' |tr -d ' '|awk -F',' '{print $1}'"
                (status,output) = commands.getstatusoutput(cmd)
#                temp = os.popen(cmd).readlines()
                if status == 0:
                    try:
                        if float(output) < float(i['key']):
                            load = output
                            flag = True
                            res = "load is ok !"
                        else:
                            load = output
                            res = "load is too high !"
                    except Exception,e:
                        print 'error:' + str(e)
                        sys.exit(2)
                elif output == "":
                    res = "can not get load !" 
                else:
                    res = res + "".join(output)
            except Exception,e:
                print 'error' + str(e)
                sys.exit(2)
        info = "".join(os.popen('/bin/echo \'' + res + '\'|/bin/gzip -9').readlines())
        if flag:
            result['result'] = 'load is ' + str(output) 
            result['status'] = '2'
            result['id'] = id
            result['time'] = time.strftime('%Y-%m-%d %H:%M',time.localtime(time.time())) 
            result['info'] = base64.encodestring(info).replace("\n","")
        else:
            result['result'] = 'load is ' + str(output)
            result['status'] = '4'
            result['id'] = id
            result['time'] = time.strftime('%Y-%m-%d %H:%M',time.localtime(time.time()))
            result['info'] = base64.encodestring(info).replace("\n","")
    else:
        result['result'] = 'no ' + server + ' mode'
        result['status'] = '4'
        result['id'] = id
        result['time'] = time.strftime('%Y-%m-%d %H:%M',time.localtime(time.time()))
        result['info'] = ""
    print str(result).replace("\'","\"")
#        print id 

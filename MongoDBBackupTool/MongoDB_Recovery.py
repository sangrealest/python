# -*- coding: utf-8 -*-
import time, calendar, shutil
import sys, os,ConfigParser, datetime

class MongoRecovery():
    def __init__(self, recoveryconfig):
        self.db_beforetime = calendar.timegm(time.gmtime())
        self.oplog_beforetime = calendar.timegm(time.gmtime())
        self.recoveryconfig = recoveryconfig
        self.host = self.recoveryconfig.get('Base', 'MongoHost')
        self.port = self.recoveryconfig.get('Base', 'MongoPost')
        self.from_db_name = self.recoveryconfig.get('Backup', 'BackupDBName')
        self.to_db_name = self.recoveryconfig.get('Recovery', 'RecoeryDBName')
        self.MongoUser = self.recoveryconfig.get('Base', 'MongoUser')
        self.MongoPW = None
        if self.MongoUser != 0:
            self.MongoPW = self.recoveryconfig.get('Base', 'MongoPaassWord')
        self.DB_BackupPath = self.recoveryconfig.get('Recovery', 'DB_BackupPath')
        self.DayBackupName = None

    def backup_oplog(self):
        NowOplog_SavePath = self.recoveryconfig.get('Recovery', 'NowOplog_SavePath')
        os.system("mongodump --host "+str(self.host)+ " --port "+ str(self.port) + " -d local -c oplog.rs " +" -o " + str(NowOplog_SavePath))

    def recovery_daybackup(self):
        file_list = os.listdir(str(self.DB_BackupPath))
        large_name = 0
        #find the latest date
        for num in range(0, len(file_list)):
            reg_num = str(file_list[num]).replace(str(self.from_db_name)+'_', '')
            if int(reg_num) > int(large_name):
                large_name = reg_num
        large_name = str(self.from_db_name)+'_'+str(large_name)
        self.DayBackupName = large_name
        os.system("mongorestore --host "+str(self.host)+ " --port "+ str(self.port) + " -d " + str(self.to_db_name) +" --drop " + str(self.DB_BackupPath) + '/' + str(large_name) + '/' + str(self.from_db_name))

    def recovery_oplog(self):
        key = 'local_'
        replayhost = self.recoveryconfig.get('Recovery', 'replayhost')
        replayport = self.recoveryconfig.get('Recovery', 'replayport')
        LastOplogName = self.recoveryconfig.get('Recovery', 'LastOplogName')
        datanum = int(str(self.DayBackupName).replace(self.from_db_name+'_', ''))
        Oplog_BackupPath = self.recoveryconfig.get('Recovery', 'Oplog_BackupPath')
        allfile_list = os.listdir(str(Oplog_BackupPath))
        re_file_list = list()
        #restore the oplog to the latest one
        for num in range(0, len(allfile_list)):
            if int(str(allfile_list[num])[len(key):len(key)+8]) >= int(datanum) and int(str(allfile_list[num])[len(key):len(key)+14]) < int(str(LastOplogName)[len(key):len(key)+14]):
                print "Oplog_BackupPath: ",Oplog_BackupPath
                print "str(allfile_list[num]): ", str(allfile_list[num])
                os.system("mongorestore --host "+str(replayhost)+ " --port "+ str(replayport) + ' -d local -c oplog.rs --drop ' + str(Oplog_BackupPath) + "/" + str(allfile_list[num]) + "/local/oplog.rs.bson")
                #replay the original replica set
                os.system("mongooplog --host "+str(self.host)+ " --port "+ str(self.port) +' -d ' + str(self.to_db_name) + ' --from ' + str(replayhost)+':'+str(replayport))

        #restore the Oplog to where error occured
        #First restore to the latest replica set
        os.system("mongorestore --host "+str(replayhost)+ " --port "+ str(replayport) +' -d local -c oplog.rs --drop ' + str(Oplog_BackupPath) + "/" + str(LastOplogName) +"/local/oplog.rs.bson")
        #restore to the time when error occured and save to Reg
        RecoryTimePoint = self.recoveryconfig.get('Recovery', 'RecoryTimePoint')
        query = '"{ts:{\$lte:'+str(RecoryTimePoint)+'}}"'
        os.system("mongodump --host "+str(replayhost)+ " --port "+ str(replayport) + " -d local -c oplog.rs -q "+ str(query) +" -o " + str(Oplog_BackupPath) + '/Reg')

        #restore Reg to replica set
        os.system("mongorestore --host "+str(replayhost)+ " --port "+ str(replayport) +' -d local -c oplog.rs --drop ' + str(Oplog_BackupPath) + "/Reg/local/oplog.rs.bson")
        #replay the original replica set
        os.system("mongooplog --host "+str(self.host)+ " --port "+ str(self.port) +' -d ' + str(self.to_db_name) + ' --from ' + str(replayhost)+':'+str(replayport))

        #delete the temp Reg
        shutil.rmtree(os.path.abspath(str(Oplog_BackupPath) + '/Reg'))


if __name__ == '__main__':
    recoveryConfig = ConfigParser.RawConfigParser()
    recoveryConfig.read('setting.config')
    recovery = MongoRecovery(recoveryConfig)
    #backup current Oplog
    recovery.backup_oplog()
    #restore to the latest one
    recovery.recovery_daybackup()
    #restore with oplog
    recovery.recovery_oplog()

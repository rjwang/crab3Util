#!/usr/bin/env python

import os,sys
import getopt
import commands

CopyRights  = '\033[92m'
CopyRights += '####################################\n'
CopyRights += '#          checkstatus.py          #\n'
CopyRights += '#       renjie.wang@cern.ch        #\n'
CopyRights += '#             May 2015             #\n'
CopyRights += '####################################\n'
CopyRights += '\033[0m'

SCRIPT = open('script_jobstatus.sh',"w")

print CopyRights

status, output = commands.getstatusoutput('ls -d crab_*')
alljobs = output.split()
#print alljobs
#print len(alljobs)
for ajob in alljobs:
	print ajob
	SCRIPT.writelines('crab status -d ' + ajob + ' --long > output_'+ajob+'.log'+';\n')


SCRIPT.close()

os.system('sh script_jobstatus.sh')


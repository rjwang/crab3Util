#!/usr/bin/env python
import os,sys
import getopt
import commands
import json

CopyRights  = '\033[92m'
CopyRights += '####################################\n'
CopyRights += '#       checkCompletedjobs.py      #\n'
CopyRights += '#       renjie.wang@cern.ch        #\n'
CopyRights += '#             May 2015             #\n'
CopyRights += '####################################\n'
CopyRights += '\033[0m'

"""
Gets the value of a given item
(if not available a default value is returned)
"""
def getByLabel(desc,key,defaultVal=None) :
    try :
        return desc[key]
    except KeyError:
        return defaultVal



SCRIPT = open('script_completedjobs.sh',"w")
BASE=os.getenv('CMSSW_BASE')
samplesDB = BASE+'/src/llvvAnalysis/DMAnalysis/data/sample_phys14.json'

#open the file which describes the sample
jsonFile = open(samplesDB,'r')
procList=json.load(jsonFile,encoding='utf-8').items()

asplit=1

status, output = commands.getstatusoutput('ls -d crab_*')
alljobs = output.split()


print CopyRights

for ajob in alljobs:
    joblog = 'output_'+ajob+'.log'
    SCRIPT.writelines('\n###################' + '\n')
    SCRIPT.writelines('# ' + ajob + '\n')
    SCRIPT.writelines('###################' + '\n\n')
    with open(joblog) as fp:

	myfinishjobs = '0.00%'
	mydir = 'FXIME'
    	for line in fp:

	  if "finished" in line:
	      for val in line.split():
	          if "%" in val: myfinishjobs=val

	  if "Task name" in line:
	      mydir = line.split(':rewang_crab_')[1].split('\n')[0]



        for proc in procList :
          for desc in proc[1] :
              data = desc['data']
              #print data
              for d in data :
                  origdtag = getByLabel(d,'dtag','')
                  split = getByLabel(d,'split','')
                  #print origdtag + ': ' + str(split)
                  if(mydir == origdtag): asplit = split
                  #print str(asplit)

        if myfinishjobs == "100.0%":
	  print mydir+": --->\033[92m " + myfinishjobs+" \033[0m<---"
          SCRIPT.writelines('#' + ajob + '\n')
          SCRIPT.writelines('  mkdir -p /tmp/rewang/'+mydir+'/results/'+';\n')
          SCRIPT.writelines('  crab getoutput -d ' + ajob + ';\n')
          SCRIPT.writelines('  mv '+ajob+'/results/*.root /tmp/rewang/'+mydir+'/results/'+';\n\n')
          #SCRIPT.writelines('# multicrab -report -c ' + ajob + ';\n')
          SCRIPT.writelines('# sh mergeOutput.sh ' + mydir + ' '+ str(asplit) + ' ;\n')
          SCRIPT.writelines('# multicrab -clean -c ' + ajob + ';\n')
          SCRIPT.writelines('# rm -r ' + ajob + ';\n')
          SCRIPT.writelines('# rm -r ' + mydir + ';\n')
          SCRIPT.writelines('# rm ' + joblog + ';\n')
	else:
	  print mydir+": --->\033[95m " + myfinishjobs+" \033[0m<---"




SCRIPT.close()

#os.system('more script_completedjobs.sh')


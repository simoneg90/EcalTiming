#! /usr/bin/env python

import os
import sys
import re
import time
import commands
import optparse
import datetime


from optparse import OptionParser

parser = OptionParser()

parser.add_option("-i", "--input", action='store', dest="rootList", help="write report to FILE", metavar="FILE", default="files.txt")
parser.add_option("-l", "--loneBunch", action='store', dest="loneBunch", help="lonebunch option", type="int", default=0)
parser.add_option("-j", "--json", action='store', dest="json", help="JSON file", metavar="FILE", default="list_tmp.txt")

parser.add_option("-L", "--Lumi", action='store', dest="Lumi", help="write report to FILE", metavar="FILE", default="list.txt")
parser.add_option("-s", "--suffix", action='store', dest="suffix", help="write report to FILE", metavar="FILE", default="")
parser.add_option("-P", "--prefix", action='store', dest="prefix",help="write report to FILE", metavar="FILE", default="outFolder")
parser.add_option("-e", "--efficiency", action='store', dest="efficiency",help="write report to FILE", metavar="FILE", default="effFile")
(opt, args) = parser.parse_args()

runList=opt.rootList #list of runs to be analyzed


for line in open(runList):
  run = [x for x in line.split()]
  print run[0]
  #os.system("cp ../test/myLauncher.sh ../test/myLauncher_"+run[0]+".sh")
  bashFile="../test/myLauncher.sh"#myLauncher.sh"#_"+run[0]+".sh"
  launchFile="myLauncher_"+run[0]+".sh"
  if opt.loneBunch==1:
    launchFile="myLauncher_loneBunch_"+run[0]+".sh"
  with open("../test/"+launchFile,'w') as new_file:
    for l in open(bashFile,"r+"):
      l = re.sub(r'RUNNUMBER=273138','RUNNUMBER='+run[0], l.rstrip())
      #new_file.write(l.replace('RUNNUMBER=273138','RUNNUMBER='+run[0]))
      if opt.loneBunch==1:
        #print "Lone Bunch"
        #new_file.write(l.replace('USAGE','RUNNUMBER'))
        l = re.sub(r'loneBunch=0','loneBunch=1', l.rstrip())
        l = re.sub(r'globaltag="80X_dataRun2_Prompt_v8"','globaltag="80X_dataRun2_HLT_v12"', l.rstrip())
        l = re.sub(r'Run2016B-v1/','Run2016B-v1/loneBunch_',l.rstrip())
      #print int(run[0])
      l = re.sub(r'globaltag="80X_dataRun2_Prompt_v8"','globaltag="80X_dataRun2_Prompt_v14"', l.rstrip())
      if int(run[0])<=273148:
        l = re.sub(r'ERA='+'"Run2016B-v1"','ERA='+'"Run2016B-v1"', l.rstrip())
      elif int(run[0])>273148 and int(run[0])<275476:
        #print int(run[0])
        l = re.sub(r'ERA='+'"Run2016B-v1"','ERA='+'"Run2016B-v2"', l.rstrip())
      elif int(run[0])>=275476 and int(run[0])<276218:
        l = re.sub(r'ERA='+'"Run2016B-v1"','ERA='+'"Run2016C-v2"', l.rstrip())
      elif int(run[0])>276218 and int(run[0])<276828:
        l = re.sub(r'ERA='+'"Run2016B-v1"','ERA='+'"Run2016D-v2"', l.rstrip())
      elif int(run[0])>276829 and int(run[0])<277430:
        l = re.sub(r'ERA='+'"Run2016B-v1"','ERA='+'"Run2016E-v2"', l.rstrip())
      elif int(run[0])>277774 and int(run[0])<=278808:
        l = re.sub(r'ERA='+'"Run2016B-v1"','ERA='+'"Run2016F-v1"', l.rstrip())
      elif int(run[0])>278808 and int(run[0])<281109:
        l = re.sub(r'ERA='+'"Run2016B-v1"','ERA='+'"Run2016G-v1"', l.rstrip())
      elif int(run[0])>281109:
        l = re.sub(r'ERA='+'"Run2016B-v1"','ERA='+'"Run2016H-v1"', l.rstrip())
      new_file.write(l+'\n')
      #os.system("cp ../test/myLauncher.sh ../test/myLauncher_"+run[0]+".sh")

  #end of with!
  os.system("chmod +x ../test/"+launchFile);
  print "Submitting job run: ",run[0], " ", launchFile
  os.system("bsub -q cmscaf1nw /afs/cern.ch/work/s/sgelli/private/CMSSW_Timing/src/EcalTiming/EcalTiming/test/"+launchFile) 


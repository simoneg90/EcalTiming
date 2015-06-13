#! /bin/bash

cd /afs/cern.ch/work/s/sgelli/public/CMSSW_7_4_4_patch4/src/

export SCRAM_ARCH='slc6_amd64_gcc491'
eval `scramv1 runtime -sh`

i=1

while read line
do
  echo "INPUT "$line
  echo "OUTPUT /afs/cern.ch/work/s/sgelli/public/CMSSW_7_4_4_patch4/src/EcalTiming/EcalTiming/test/output"$i".root"
  cmsRun /afs/cern.ch/work/s/sgelli/public/CMSSW_7_4_4_patch4/src/EcalTiming/EcalTiming/test/ecalTime_fromAlcaStream_cfg.py files="$line" output="/afs/cern.ch/work/s/sgelli/public/CMSSW_7_4_4_patch4/src/EcalTiming/EcalTiming/test/output/outFile"$i".root"
  let i++

done</afs/cern.ch/work/s/sgelli/public/CMSSW_7_4_4_patch4/src/EcalTiming/EcalTiming/test/file.txt

RUNLIST="243479 243484 243506"
for RUN in ${RUNLIST}
do

echo "=== RUN = ${RUN}"
filelist=`das_client.py --query="file dataset=/MinimumBias/Commissioning2015-v1/RAW run=${RUN}" --limit=50 | sed '2 d'`
for file in ${filelist}
do
das_client.py --query="file=${file} | sum(file.nevents)"
done
filelist=`echo ${filelist}| sed 's| |,|g;s|,$||'`
echo ${filelist}

bsub -q 1nd "cd $PWD; eval \`scramv1 runtime -sh\`; cmsRun python/ecalTimeTreeMaker_FromRaw_CosmicOrBeamSplash_cfg.py files=${filelist} output=ecalTiming-${RUN}.root maxEvents=-1"

exit 0
cat > test/run-${RUN}.cfg <<EOF
[CRAB]
jobtype=cmssw
scheduler=CAF

		
[CMSSW]
datasetpath=/MinimumBias/Commissioning2015-v1/RAW
runselection=${RUN}
pset=python/ecalTimeTreeMaker_FromRaw_CosmicOrBeamSplash_cfg.py
get_edm_output=1
#split_by_run=1
lumis_per_job=10000
total_number_of_lumis=-1
#number_of_jobs=1

[USER]
ui_working_dir=/afs/cern.ch/user/s/shervin/scratch1/CMSSW_7_3_4/src/CalibCalorimetry/EcalTiming/test/run-${RUN}
return_data=1
#outputdir=/afs/cern.ch/user/s/shervin/scratch1/CMSSW_7_3_4/src/CalibCalorimetry/EcalTiming/test/run-${RUN}/output
check_user_remote_dir=1

[CAF]
queue=cmscaf1nd



[GRID]



EOF

done

RUNLIST="243479 243484 243506"
RUNLIST="248030"
RUNLIST=`cat runlist`
STREAM=AlCaPhiSym
NEVENTS=-1

for i in "$@"
do
case $i in
    -s=*|--stream=*)
    STREAM="${i#*=}"
    shift # past argument=value
    ;;
    -r=*|--runlist=*)
    RUNLIST="${i#*=}"
	 RUNLIST=${RUNLIST//,/ }
    shift # past argument=value
    ;;
    -n=*|--nevents=*)
    NEVENTS="${i#*=}"
    shift # past argument=value
    ;;
    -b|--batch)
    BATCH=YES
    shift # past argument with no value
    ;;
    *)
            # unknown option
		echo option $i not defined
    ;;
esac
done

for RUN in ${RUNLIST}
do

	echo "=== RUN = ${RUN}"
	OUTDIR=output/${STREAM}-${RUN}/
	mkdir -p ${OUTDIR}

	#filelist=`das_client.py --query="file dataset=/MinimumBias/Commissioning2015-v1/RAW run=${RUN}" --limit=50 | sed '2 d'`
	nfiles=`das_client.py --query="file dataset=/AlCaPhiSym/Run2015B-v1/RAW run=${RUN} | count(file.name)" | sed '2 d'`
	nfiles=${nfiles:19}

	if ! [[ $nfiles =~ ^[0-9]+$ ]]; then
		echo "No Files found"
		exit 1
	fi

	echo Will run over $nfiles files
	filelist=`das_client.py --query="file dataset=/AlCaPhiSym/Run2015B-v1/RAW run=${RUN}" --limit=${nfiles} | sed '2 d'`
	# for file in ${filelist}
	# do
	# das_client.py --query="file=${file} | sum(file.nevents)"
	# done

	filelist=`echo ${filelist}| sed 's| |,|g;s|,$||'`
	echo ${filelist}

	jsonFile=/afs/cern.ch/user/p/phansen/public/ecal-timing/ECALJSON/files/Cert_All_13TeV_PromptReco_Collisions15_ECALonly_JSON.txt
	if [ "$BATCH" == "YES" ]
	then
		bsub -oo ${OUTDIR}/stdout.log -eo ${OUTDIR}/stderr.log -R "rusage[mem=4000]" -q 2nd "cd $PWD; eval \`scramv1 runtime -sh\`; 
		cmsRun test/ecalTime_fromAlcaStream_cfg.py files=${filelist} output=${OUTDIR}/ecalTiming-${RUN}-lsf.root maxEvents=${NEVENTS}
		jsonFile=${jsonFile}
		" || exit 1
	else
		cmsRun test/ecalTime_fromAlcaStream_cfg.py files=${filelist} output=${OUTDIR}/ecalTiming-${RUN}.root maxEvents=${NEVENTS} \
		jsonFile=${jsonFile}
	fi

done
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
ui_working_dir=/afs/cern.ch/user/s/shervin/scratch1/CMSSW_7_3_4/src/EcalTiming/EcalTiming/test/run-${RUN}
return_data=1
#outputdir=/afs/cern.ch/user/s/shervin/scratch1/CMSSW_7_3_4/src/EcalTiming/EcalTiming/test/run-${RUN}/output
check_user_remote_dir=1

[CAF]
queue=cmscaf1nd



[GRID]



EOF

done

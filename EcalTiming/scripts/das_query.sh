runlist=`cat runlist`

for RUN in $runlist
do
	echo ===$RUN===
	das_client.py --query="summary dataset=/AlCaPhiSym/Run2015B-v1/RAW run=${RUN}"
done

echo === FILE SUMMARY ===
for RUN in $runlist
do
	filelist=$(das_client.py --limit=1000 --query="file dataset=/AlCaPhiSym/Run2015B-v1/RAW run =$RUN" | grep store)
	for file in $filelist
	do
		lumis=$(das_client.py --query="lumi file=$file" | grep "\[")
		lumis=${lumis// /}
		nevents=$(das_client.py --query="file=$file |sum(file.nevents)" |grep nevents)
		nevents=${nevents:18}
		echo $RUN $lumis $nevents $file
	done
done

runlist=`cat runlist`

for RUN in $runlist
do
	filelist=$(das_client.py --query="file dataset=/AlCaPhiSym/Run2015B-v1/RAW run =$RUN" | grep store)
	for file in $filelist
	do
		lumis=$(das_client.py --query="lumi file=$file" | grep "\[")
		lumis=${lumis// /}
		echo $RUN $lumis $file
	done
done

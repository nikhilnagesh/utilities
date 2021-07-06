#!/bin/bash

clear
#Fetch the running workflow job name from oozie
oozieWf=`oozie jobs -filter status=RUNNING 2>/dev/null | cut -d ' ' -f1 | grep 0000*`

runningJobCount=`echo $oozieWf | wc -w`

if [[ "$runningJobCount" -eq 1 ]]; 
then 
	if [ ! -z "$oozieWf" -a "$oozieWf" != " " ]; then
	echo "Currently `echo $oozieWf` is in RUNNING"
	#Printing the oozie job status to console every 7 seconds 
	while sleep 7;do clear ;oz="oozie job -info `echo $oozieWf`";$oz 2>/dev/null;done
	fi
fi

if [[ "$runningJobCount" -eq 0 ]]; 
then
echo "There are no oozie jobs in RUNNING status"
exit 0 
fi

if [[ "$runningJobCount" -ge 1 ]]; 
then
echo "There are more than one oozie jobs in RUNNING status"
exit 1 
fi

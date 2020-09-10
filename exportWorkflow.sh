#!/bin/bash

##################################################################################################################################
#  Program Name         : exportWorkflow.sh
#  Brief Description    : This script is used to export the workflow from repository and check the coding 
#                         standards of Workflow, session and mapping
#  Author               : Nikhil Nagesh
#  Email                : Nikhil.Nagesh@evry.com
#  Created Date         : 2020-26-08
#  Last Modified Date   : 2020-10-09
#  Executing method     : ./exportWorkflow.sh userid workflowName repoFolderName
#  Additional Arguments : None
#  Property Files used  : None
###################################################################################################################################

source /etc/profile
source /home/infsvc/.profile
source /home/db2inst1/sqllib/db2profile
export INFA_HOME=/home/infsvc/Informatica/PowerCenter
export LD_LIBRARY_PATH=/home/infsvc/Informatica/PowerCenter/server/bin
export integrationSerivce="repo_dalgridtest"
export informaticaDomain="Domain_infatest"

execPath=`pwd`
username=${1}  #UserName
uinput=${2} #WorkflowName
finput=${3} #FolderName
clear

echo -n "Please Enter Password                                   :"; read -s p 
password=$p
clear

#Connect to dev repository
$INFA_HOME/server/bin/pmrep connect -r ${integrationSerivce} -d ${informaticaDomain} -n ${username} -s "Infa Users" -x "${password}" > /dev/null
#clear

#  Verify whether connection was successful or not
if [ $? -ne 0 ]
    then 
    clear
    echo -ne 'Could not connect... user name or password may be invalid.\n'
    exit 1
fi
echo 'Succesfully connected to repository...'


WORKFLOWS=`$INFA_HOME/server/bin/pmrep listobjects -o workflow -f ${finput} | grep workflow | sed 's/workflow//g' | grep $uinput`

if [[ ! -z ${WORKFLOWS} ]]; then
    for WORKFLOW in ${WORKFLOWS}; do
        if [ ${uinput} = ${WORKFLOW} ]; then
             echo -ne "Exporting workflow\t: ${WORKFLOW}\n"
             $INFA_HOME/server/bin/pmrep objectexport -o workflow -f ${finput} -n ${WORKFLOW} -m -s -b -r -u ${WORKFLOW}.XML  > /dev/null
             echo -ne "Export\t\t\t: Complete\n"
             sleep 1
             clear
        fi
    done
else
    echo -ne "Workflow not found, please verify the workflow/folder names.\n"
    exit 1
fi

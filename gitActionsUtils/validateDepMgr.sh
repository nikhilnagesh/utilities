#!/bin/bash

#Shell Script to validate the first three lines of hms_deployment_manager

workdir=$1
file_name=${workdir}/hms_deployment_manager.txt

content1=$(
  sed '
    s/[[:space:]]\{1,\}/ /g; # turn sequences of spacing characters into one SPC
    s/[^[:print:]]//g; # remove non-printable characters
    s/^ //; s/ $//; # remove leading and trailing space
    q; # quit after first line' < "$file_name"
)

echo $content1

content2=$(
  sed -n '2{p;q}' < "$file_name"
)

echo $content2

content3=$(
  sed -n '3{p;q}' < "$file_name"
)

echo $content3

################################################
# Verify the first three lines

if [ "$content1" = 'DO NOT REMOVE FIRST THREE LINES' ]; then
  echo 'Test Success - 1st line is proper'
else
echo 'Test Failed - 1st line is not proper in hms_deployment_manager.txt'
exit 1
fi

if [ "$content2" = 'example: <CHANGE_NUMBER>:<WORKFLOW_FILE.xml>:<CONTROL_FILE.xml>:<integration_service>' ]; then
  echo 'Test Success - 2nd line is proper'
else
echo 'Test Failed - 2nd line is not proper in hms_deployment_manager.txt'
exit 1
fi

if [[ "$content3" =~ ^----- ]]; then
  echo 'Test Success - 3rd line is proper'
else
echo 'Test Failed - 3rd line is not proper in hms_deployment_manager.txt'
exit 1
fi
###################################################

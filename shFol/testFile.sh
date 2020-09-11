#!/bin/bash

GITHUB_WORKSPACE=$1
file_name=${GITHUB_WORKSPACE}/hms_deployment_manager.txt

content=$(
  sed '
    s/[[:space:]]\{1,\}/ /g; # turn sequences of spacing characters into one SPC
    s/[^[:print:]]//g; # remove non-printable characters
    s/^ //; s/ $//; # remove leading and trailing space
    q; # quit after first line' < "$file_name"
)

if [ "$content" = 'DO NOT REMOVE FIRST THREE LINES' ]; then
  echo 'Test Success'
else
echo 'Test Failed - hms_deployment_manager.txt is not correct'
exit 1
fi

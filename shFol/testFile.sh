#!/bin/bash

in_arg=$1
file_content=`cat $1`

case $file_content in
  (*DO NOT REMOVE FIRST THREE LINES*)
     echo "hms_deployment_manager file is good for running CI/CD"
     ;;  
  (*)
     echo "hms_deployment_manager file is not good"
     exit(1)
esac

#!/bin/bash

$file_content=`cat /utilities/hms_deployment_manager.txt`

case $file_content in
  (*DO NOT REMOVE FIRST THREE LINES*)
     echo "hms_deployment_manager file is good for running CI/CD"
     ;;  
  (*)
     echo "hms_deployment_manager file is not good"
     exit(1)
esac

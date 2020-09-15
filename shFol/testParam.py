##################################################################################################################################
#  Program Name: validateParam.py
#  Brief Description:
#  Author: Nikhil Nagesh
#  Email: Nikhil.Nagesh@evry.com
#  Created Date:  08/26/2020
#  Last Modified Date: 09/15/2020
#  Executing method: 
#  Additional Arguments: None
#  Property Files used: None
###################################################################################################################################

###################################################################################################################################
#  Importing required libraries
###################################################################################################################################
import os
import time as t
import logging
import xml.etree.ElementTree as ET
import re
import sys
from datetime import datetime
import pathlib

#######################################################################################################################################
#  Global Variables
#######################################################################################################################################
vgTxtFmt = 100
vgWriteFmt = 90
vgInfoFmt = 50

#######################################################################################################################################
#  Input Arguments
#######################################################################################################################################



#######################################################################################################################################
#  Config Folders Read, Report Files and Log files creation
#######################################################################################################################################

vlCurWrDir = os.getcwd()


#######################################################################################################################################
#  Methods section
#######################################################################################################################################

def func_ValidateParam(arg_ParamFile):
    # global vlErroCntr
    for iLnNum, iLines in enumerate(arg_ParamFile, 1):
        iLine = iLines.strip()
        for vlKey in iLine.split():
            if re.match("(.*)DBConnection_SOURCE(.*)", vlKey):
                if vlKey[vlKey.find('=') + 1:].upper() == 'ECPROD_EXHMS3':
                    print(
                        "Source Connections pointing to production - PASS")
                else:
                    print(
                        "Line Number :{} Connection {} is not proper - FAILED".
                        format(iLnNum, vlKey))
                    sys.exit(1)
            if re.match("(.*)DBConnection_TARGET(.*)", vlKey):
                if vlKey[vlKey.find('=') + 1:].upper(
                ) == 'ECPROD_EXHMS3' or vlKey[vlKey.find('=') +
                                              1:] == 'PowerExchange_DPXINFA':
                    print(
                        "Target Connections pointing to production - PASS")
                else:
                    print(
                        "Line Number :{} Connection {} is not proper - FAILED".
                        format(iLnNum, vlKey))
                    sys.exit(1)
            if re.match("(.*)BaseFileDSN(.*)", vlKey):
                if vlKey[vlKey.find('=') + 1:].startswith('P.HMS.TPL'):
                    print("BaseFileDSN starts with P.HMS.TPL. - PASS")
                else:
                    print(
                        "Line Number :{} FileDSN {} is not proper - FAILED".
                        format(iLnNum, vlKey))
                    sys.exit(1)
            if re.match("(.*)TargetFileDSN(.*)", vlKey):
                if vlKey[vlKey.find('=') + 1:].startswith('"P.HMS.TPL'):
                    print("TargetFileDSN starts with P.HMS.TPL. - PASS")
                else:
                    print(
                        "Line Number :{} FileDSN {} is not proper - FAILED".
                        format(iLnNum, vlKey))
                    sys.exit(1)


#######################################################################################################################################
#  Main section
#######################################################################################################################################


def main():
    #Read the param file
    vlParamDir=vlCurWrDir+'/param/Provider'
    currentDirectory = pathlib.Path(vlParamDir)
    filePattern = '*.ini'
    for currFile in currentDirectory.glob(filePattern):
        try:
            vlOpenFile = open(vlParamDir + '/' + str(currFile), 'r')
            # print("Parameter file read successful")
        except IOError:
            print("Failed to read the parameter file ".ljust(vgWriteFmt, ' ') +
                  ":{}\n".format(str(currFile)))
            sys.exit(1)
        # Call the method to validate parameter file
        func_ValidateParam(vlOpenFile)


if __name__ == "__main__":
    main()

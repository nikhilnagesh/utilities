##################################################################################################################################
#  Program Name: validateParam.py
#  Brief Description:
#  Author: Nikhil Nagesh
#  Email: Nikhil.Nagesh@evry.com
#  Created Date:  08/26/2020
#  Last Modified Date: 09/10/2020
#  Executing method: python validateParam.py PROVIDER w_127_B4T_101_LOAD_ACTIVITY_REC_STG 127_B4T_PROVIDER
#                    python validateParam.py RESOURCE wf_SET_445_RSC_V1 SET_445_RSC_V1
#                    python validateParam.py PRESTAGE wf_XKTX3TNRX_V1_ClmsPro_SRC_2_PSTG XKTX3TNRX_V1_ClmsPro_src2pstg
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

#######################################################################################################################################
#  Global Variables
#######################################################################################################################################
vgTxtFmt = 100
vgWriteFmt = 90
vgInfoFmt = 50

#######################################################################################################################################
#  Input Arguments
#######################################################################################################################################
# vlUserName = os.getlogin()
#
#--------> Debug Commented: To Manually run the workflow without passing arguments.
#
# vlArgCheck = len(sys.argv) - 1
# if vlArgCheck < 3:
    # print(
        # "Insufficient arguments passed. \n The code takes exactly 3 parameters \n Parameter 1: Process name\n Parameter 2: Worklfow name \n Parameter 3: Parameter file name\n"
    # )
    # print("Usage :- python " + sys.argv[0] +
          # " process_name workflow_name parameter_name")
    # sys.exit(1)
# else:
    # pProc = sys.argv[1]
    # pWfFileName = sys.argv[2]
    # pParam = sys.argv[3]
#
#--------> Debug Add   
#
pProc = 'PROVIDER'
pWfFileName = 'w_818_X3T_101_LOAD_ACTIVITY_REC_STG'
pParam = '818_X3T_PROVIDER'

#######################################################################################################################################
#  Config Folders Read, Report Files and Log files creation
#######################################################################################################################################
vlLogDir = "logs"
vlRptDir = "reports"
vlCurWrDir = os.getcwd()
vlLogPath = os.path.join(vlCurWrDir, vlLogDir)
vlRptPath = os.path.join(vlCurWrDir, vlRptDir)
vlLogFileNm = sys.argv[0].split(
    '.')[0] + '_' + pProc + '_' + pWfFileName + '_' + pParam + '.log'
vlDateTime = str(datetime.utcnow().strftime('%Y-%m-%d %I:%M:%S'))
#
#--------> Debug Commented
#
# if os.path.isfile(vlCurWrDir+'/'+pWfFileName+'.XML'):
    # os.remove(vlCurWrDir+'/'+pWfFileName+'.XML')
# if not os.path.exists(vlLogPath):
    # os.makedirs(vlLogPath, mode=0755)
# if not os.path.exists(vlRptPath):
    # os.makedirs(vlRptPath, mode=0755)
vlErroCntr = 0
#vlRptName = pProc + '_' + pWfFileName + '_' + pParam + '_' + 'SummaryReport.txt'
vlRptName = 'SummaryReport.txt'
vlReport = open(vlRptName, "w+")

#######################################################################################################################################
#  Logger and Levels
#######################################################################################################################################
LEVELS = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL
}

if len(sys.argv) < 2:
    level_name = 'info'
    level = LEVELS.get(level_name, logging.INFO)
    logging.basicConfig(
        format='%(asctime)s  - %(levelname)-7s >>> %(message)s',
        datefmt='%y%y-%m-%d %H:%M:%S',
        filename=vlLogFileNm,
        filemode='w+',
        level=level)

elif len(sys.argv) > 1:
    level_name = sys.argv[1]
    level = LEVELS.get(level_name, logging.NOTSET)
    logging.basicConfig(
        format='%(asctime)s  - %(levelname)-7s >>> %(message)s',
        datefmt='%y%y-%m-%d %H:%M:%S',
        filename=vlLogFileNm,
        filemode='w+',
        level=level)


#######################################################################################################################################
#  Methods section
#######################################################################################################################################
def test_func_Proc(pProc):
    return {
        'provider': 'tst_provider',
        'providerloads': 'tst_provider',
        'provider_loads': 'tst_provider',
        'resource': 'RESOURCE_LOADS',
        'resourceloads': 'RESOURCE_LOADS',
        'resource_loads': 'RESOURCE_LOADS',
        'prestage': 'CLAIMS_PRESTG',
        'ccdbprestage': 'CLAIMS_PRESTG',
        'ccdb_prestage': 'CLAIMS_PRESTG',
        'reformat': 'CLAIMS_REFORMAT',
        'ccdbreformat': 'CLAIMS_REFORMAT',
        'ccdb_reformat': 'CLAIMS_REFORMAT',
        'client': 'EE_Client_Load',
        'clientloads': 'EE_Client_Load',
        'client_loads': 'EE_Client_Load'
    }[pProc]


def test_func_ValidateParam(arg_ParamFile):
    global vlErroCntr
    for iLnNum, iLines in enumerate(arg_ParamFile, 1):
        iLine = iLines.strip()
        for vlKey in iLine.split():
            if re.match("(.*)DBConnection_SOURCE(.*)", vlKey):
                if vlKey[vlKey.find('=') + 1:].upper() == 'ECPROD_EXHMS3':
                    logging.info(
                        "Source Connections pointing to production - PASS")
                    vlReport.write(vlKey.
                                   ljust(vgWriteFmt, ' ') +
                                   " {}\n".format(':PASS'))
                else:
                    logging.error(
                        "Line Number :{} Connection {} is not proper - FAILED".
                        format(iLnNum, vlKey))
                    vlReport.write(vlKey.
                                   ljust(vgWriteFmt, ' ') +
                                   " {}\n".format(':FAILED'))
                    vlReport.write("       >>> Reason: Invalid "+vlKey[vlKey.find('=') + 1:]+"\n")
                    vlErroCntr += 1
            if re.match("(.*)DBConnection_TARGET(.*)", vlKey):
                if vlKey[vlKey.find('=') + 1:].upper(
                ) == 'ECPROD_EXHMS3' or vlKey[vlKey.find('=') +
                                              1:] == 'PowerExchange_DPXINFA':
                    logging.info(
                        "Target Connections pointing to production - PASS")
                    vlReport.write(vlKey.
                                   ljust(vgWriteFmt, ' ') +
                                   " {}\n".format(':PASS'))
                else:
                    logging.error(
                        "Line Number :{} Connection {} is not proper - FAILED".
                        format(iLnNum, vlKey))
                    vlReport.write(vlKey.
                                   ljust(vgWriteFmt, ' ') +
                                   " {}\n".format(':FAILED'))
                    vlReport.write("       >>> Reason: Invalid "+vlKey[vlKey.find('=') + 1:]+"\n")
                    vlErroCntr += 1
            if re.match("(.*)BaseFileDSN(.*)", vlKey):
                if vlKey[vlKey.find('=') + 1:].startswith('P.HMS.'):
                    logging.info("BaseFileDSN starts with P.HMS.TPL. - PASS")
                    vlReport.write(vlKey.ljust(
                        vgWriteFmt, ' ') + " {}\n".format(':PASS'))
                else:
                    logging.error(
                        "Line Number :{} FileDSN {} is not proper - FAILED".
                        format(iLnNum, vlKey))
                    vlReport.write(vlKey.ljust(
                        vgWriteFmt, ' ') + " {}\n".format(':FAILED'))
                    vlReport.write("       >>> Reason: Invalid "+vlKey[vlKey.find('=') + 1:]+"\n")
                    vlErroCntr += 1
            if re.match("(.*)TargetFileDSN(.*)", vlKey):
                if vlKey[vlKey.find('=') + 1:].startswith('"P.HMS.'):
                    logging.info("TargetFileDSN starts with P.HMS.TPL. - PASS")
                    vlReport.write(vlKey.ljust(
                        vgWriteFmt, ' ') + " {}\n".format(':PASS'))
                else:
                    logging.error(
                        "Line Number :{} FileDSN {} is not proper - FAILED".
                        format(iLnNum, vlKey))
                    vlReport.write(vlKey.ljust(
                        vgWriteFmt, ' ') + " {}\n".format(':FAILED'))
                    vlReport.write("       >>> Reason: Invalid "+vlKey[vlKey.find('=') + 1:]+"\n")
                    vlErroCntr += 1


def test_func_WorkflowPropCheck(arg_ParsedXml):
    global vlErroCntr
    for node in arg_ParsedXml.iter('WORKFLOW'):
        for snode in node:
            if snode.tag == 'ATTRIBUTE' and snode.attrib[
                    'NAME'] == 'Parameter Filename':
                if snode.attrib['VALUE'] == '' or snode.attrib['VALUE'] is None:
                    logging.error(
                        'Parameter file or path doesn\'t exist in workflow\'s session :{}'
                        .format(':FAILED'))
                    vlReport.write(
                        "Parameter file or path doesn\'t exist in workflow\'s session".ljust(
                            vgWriteFmt, ' ') + " {}\n".format(':FAILED'))
                    vlErroCntr += 1
                else:
                    logging.info(snode.attrib['NAME'] + " with full path:\n" +
                                 snode.attrib['VALUE'])
                    vlReport.write(
                        snode.attrib['NAME'] + " with full path:\n" +
                                 snode.attrib['VALUE']
                        .ljust(vgWriteFmt, ' ') + " {}\n".format(':PASS'))

#######################################################################################################################################
#  Main section
#######################################################################################################################################


def test_main():
    logging.info("Run Date/Time: {}".format(vlDateTime))
    logging.info("User Name: {}".format(vlUserName))
    logging.info("Process Name: {}".format(pProc))
    logging.info("Current Working Directory: {}".format(vlCurWrDir))
    logging.info("Logging Directory: {}".format(vlLogPath))

    vlReport.write("".center(vgTxtFmt, '-') + "\n")
    vlReport.write(
        "Parameter File Validation and Test Results.".center(vgTxtFmt, '-') +
        "\n")
    vlReport.write("\n")
    vlReport.write("Run Date/Time".ljust(vgInfoFmt, ' ') +
                   " :{}\n".format(vlDateTime))
    vlReport.write("\n")
    vlReport.write("User ID".ljust(vgInfoFmt, ' ') +
                   " :{}\n".format(vlUserName))
    vlReport.write("\n")
    vlReport.write("Process".ljust(vgInfoFmt, ' ') + " :{}\n".format(pProc))
    vlReport.write("\n")
    vlReport.write("Workflow".ljust(vgInfoFmt, ' ') +
                   " :{}\n".format(pWfFileName))
    vlReport.write("\n")
    vlReport.write("Param File".ljust(vgInfoFmt, ' ') +
                   " :{}\n".format(pParam))
    vlReport.write("".center(vgTxtFmt, '-') + "\n")
    vlReport.write("\n")

    try:
        vlProc = pProc.lower()
        vlRepoFol = test_func_Proc(vlProc)
    except:
        print(
            "The {} is unknown for the tool, test cases may be inappropriate".
            format(pProc))
        vlRepoFol = pProc
#--------> Debug Add
    # vlCmd = "%s %s %s %s" % (vlCurWrDir + '/exportWorkflow.sh', vlUserName,
                             # pWfFileName, vlRepoFol)

    # #Invoke the shell script to fetch the workflow xml file from repository
    # os.system(vlCmd)

    #Read the param file
    try:
        vlOpenFile = open(vlCurWrDir + '/' + pParam + '.ini', 'r')
        logging.info("Parameter file read successful")
    except IOError:
        print("Failed to read the parameter file ".ljust(vgWriteFmt, ' ') +
              ":{}\n".format(pParam + '.ini'))
        print("Please place the parameter file in".ljust(vgWriteFmt, ' ') +
              " :{}\n".format(vlCurWrDir))
        logging.error('Failed to read the parameter file :{}'.format(pParam +
                                                                     '.ini'))
        vlReport.close()
        os.remove(vlRptPath + '/' + vlRptName)
        sys.exit(1)

    # Read the xml file
    try:
        vlOpenWfFile = open(vlCurWrDir + '/' + pWfFileName + '.XML', 'r')
        logging.info("Workflow file read successful")
    except IOError:
        print("Failed to read the workflow xml file ".ljust(vgWriteFmt, ' ') +
              ":{}\n".format(pWfFileName + '.XML'))
        logging.error(
            'Failed to read the workflow xml file :{}'.format(pWfFileName +
                                                              '.XML'))
        sys.exit(1)

    #Parse the xml file
    try:
        vlXmlTree = ET.parse(vlOpenWfFile)
        logging.info("Workflow parsing was successful")
    except ET.ParseError:
        print(" Failed to read the xml : " + pWfFileName +
              ".\n It is either corrupted or invalid. Please verify \n")
        logging.error('Failed to read the xml file :{}'.format(pWfFileName +
                                                               '.XML'))
        vlReport.close()
        os.remove(vlRptPath + '/' + vlRptName)
        sys.exit(1)

    # Call the method to validate parameter file
    test_func_ValidateParam(vlOpenFile)

    # Call the method to validate param path in workflow
    test_func_WorkflowPropCheck(vlXmlTree)

    vlReport.write("".center(vgTxtFmt, '-') + "\n")

    global vlErroCntr
    logging.info("Overal test results".center(vgTxtFmt, '-'))
    if vlErroCntr > 0:
        logging.critical("One or more test results are FAILED")
        vlReport.write("\n")
        vlReport.write("Overall validation result".ljust(vgWriteFmt, ' ') +
                       " :{}\n".format('FAILED'))
        print("".center(vgTxtFmt, '-') + "\n")
        print("Overall validation results".ljust(vgWriteFmt, ' ') +
              " :{}\n".format('FAILED'))
        print("Please download the reports from".ljust(vgWriteFmt, ' ') +
              " :{}\n".format(vlRptPath))
        print("".center(vgTxtFmt, '-') + "\n")
        vlReport.write("\n")
        vlReport.write("".center(vgTxtFmt, '-') + "\n")
    else:
        logging.info("All Validations have PASSED")
        vlReport.write("\n")
        vlReport.write("Overall validation result".ljust(vgWriteFmt, ' ') +
                       " :{}\n".format('PASS'))
        print("".center(vgTxtFmt, '-') + "\n")
        print("Overall validation results".ljust(vgWriteFmt, ' ') +
              " :{}\n".format('PASSED'))
        print("Please download the reports from".ljust(vgWriteFmt, ' ') +
              " :{}\n".format(vlRptPath))
        print("".center(vgTxtFmt, '-') + "\n")
        vlReport.write("\n")
        vlReport.write("".center(vgTxtFmt, '-') + "\n")

    vlReport.close()

    logging.info("".center(vgTxtFmt, '-'))


if __name__ == "__main__":
    test_main()

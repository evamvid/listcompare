import xlrd
import configparser
import os
import xlsxwriter
import itertools
import csv
import codecs
import io

#needs a config.txt with section Main and variables 'list_checkfrom' and 'list_checkagainst' and 'column'
#also needs section "Excel" with variable "sheet," indexed at 0
#header variable in main describes whether the first row is column headers or not

class invalidFileType(Exception):
    pass

def namenumberconvert(name):
    stop = False
    while (stop == False):
        for i in itertools.count():
            name = xlsxwriter.utility.xl_col_to_name(i)
            if (name == column):
                return(i)
                stop = True
#be warned: the variables bigList and SmallList are actually filename strings; these should probably be changed to not be confusing
Config = configparser.ConfigParser()
Config.read('config.txt')
bigList= Config.get('Main', 'list_checkfrom')
smallList = Config.get('Main', 'list_checkagainst')
column = Config.get('Main', 'column')
excelSheet = Config.getint('Excel', 'sheet')
header = Config.getboolean('Main', 'header')
mode = Config.getint('Main', 'mode')

column = namenumberconvert(column)

print(bigList)
print(smallList)

listList = [bigList, smallList]

'''
for x in [0,1]:
    ext = os.path.splitext(listList[x])
    if ext != '.xlsx' and ext != '.csv':
        raise invalidFileType(listList[x] + 'File not csv or xlsx')
    else:
        pass  
'''   
 
#needs parsecsv and parseexcel functions that return lists of the contents    
def parsecsv(file):
    results = []
    with open(file, mode='r',  encoding='ISO-8859-1') as f:
    #with codecs.open(file, "r",encoding='ISO-8859-1', errors='ignore') as fdata:
         reader = csv.reader((x.replace('\0', '') for x in f), delimiter = ',')#generator to replace null bytes
         for x in reader:
             print("hello" + str(x))
             results.append(x[column])
    return(results)

def parsexlsx(file):
    results = []
    with open(file, 'rb') as f:
        reader = xlrd.open_workbook(file)
        sheet = reader.sheet_by_index(int(excelSheet))
        if header == True:
            results = sheet.col_values(column, 1)
        elif header == False:
            results == sheet.col_values(column)
    return(results)

                
if bigList.endswith('.csv'):
    blistparsed = parsecsv(bigList)
elif bigList.endswith('xlsx'):
    blistparsed = parsexlsx(bigList)

if smallList.endswith('.csv'):
    slistparsed = parsecsv(bigList)
elif smallList.endswith('xlsx'):
    slistparsed = parsexlsx(bigList)
    
#needs functions that do the actual computation for different modes    

def modeZero(smallList, bigList):
    newSmallList = list(smallList)
    newBigList = list(bigList)
    for item in newBigList:
        if item in newSmallList:
            newBigList.remove(item)
        else:
            pass
    return(newBigList)
def modeOne(smallList, bigList):
    newSmallList = list(smallList)
    newBigList = list(bigList)
    resultList = []
    for item in newSmallList:
        if item in newBiglist:
            resultList.append(item)
        else:
            pass
    return(resultList)

def modeTwo(smallList, bigList):    
    newSmallList = list(smallList)
    newBigList = list(bigList)
    resultList = []
    for item in newSmallList:
        if item in newBigList:
            pass
        elif item not in newBigList:
            resultList.append(item)
    return(resultList)
    
if (mode == 0):
    result = modeZero(slistparsed, blistparsed)
elif (mode == 1):
    result = modeOne(slistparsed, blistparsed)
elif(mode == 2):
    result = modeTwo(slistparsed, blistparsed)

print(result)

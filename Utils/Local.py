from pandas import read_excel, read_csv
import numpy as np
import os
import pandas as pd
from datetime import datetime

import pickle

from Utils.Constants import LocalDataConstants

def ExperimentDataLoader():

    BehavioralData = read_excel(LocalDataConstants.directories['beh_dir_file'])
    Performance_data = read_csv(LocalDataConstants.directories['perform_data_dir'])

    return BehavioralData, Performance_data

def AvailableSubjects():

    SOI = np.load(LocalDataConstants.directories['ListOfAvailableSubjects'])

    return SOI

def HandleDir(Directory):

    if not os.path.isdir(Directory):

        os.makedirs(Directory)

    return Directory

def HandleFileName(SaveFileDir, specs):

    CurrentTime = datetime.now()

    if not os.path.isfile(SaveFileDir + "\\VersionHistory.csv"):

        HistoryDict = {'idx': 0, 'VersionNumber': [0], 'Date': [str(CurrentTime.year) + '-' + str(CurrentTime.month) + '-' + str(CurrentTime.day)], 
                       'Window_Length': [specs['window_length']], 'Overlap_Ratio': [specs['overlap_ratio']], 'Start Time': [specs['start time']],
                       'End Time': [specs['end time']],
                       'OrdersMatrix': [specs['orders_matrix']]}
        DF = pd.DataFrame(HistoryDict)

        DF.to_csv(SaveFileDir + "\\VersionHistory.csv", index = False)

        version_number = 0

    else:

        HistoryDict = read_csv(SaveFileDir + "\\VersionHistory.csv", index_col = 0)

        version_number = HistoryDict['VersionNumber'][len(HistoryDict['VersionNumber']) - 1] + 1

        new_row = [version_number, str(CurrentTime.year) + '-' + str(CurrentTime.month) + '-' + str(CurrentTime.day), specs['window_length'],
                   specs['overlap_ratio'], specs['start time'], specs['end time'], specs['orders_matrix']]
        
        HistoryDict.loc[len(HistoryDict['VersionNumber'])] = new_row
        HistoryDict.sort_index()

        HistoryDict.to_csv(SaveFileDir + "\\VersionHistory.csv")

    SaveFileName = "Data_Version" + str(version_number)

    return SaveFileName, version_number
    
def HandleDataLoad(Dir, version_number = None):

    assert os.path.isdir(Dir), "This Data is not Available"

    if version_number is None:

        VersionHistoryDF = read_csv(Dir + "\\VersionHistory.csv", index_col = 0)
        version_number = np.array(VersionHistoryDF['VersionNumber'])[-1]

    LoadFileDir = Dir + "\\Data_Version" + str(version_number)

    with open(LoadFileDir, 'rb') as f:

        ConDataDict = pickle.load(f)

    return ConDataDict

def TimeToSample(TimeWin, specs = {'ZeroPoint': 25, 'Fs': 250}):

    ZP = specs['ZeroPoint']
    Fs = specs['Fs']

    SP = int(TimeWin[0] * (Fs / 1000) + ZP)
    FP = int(TimeWin[1] * (Fs / 1000) + ZP)

    return SP, FP
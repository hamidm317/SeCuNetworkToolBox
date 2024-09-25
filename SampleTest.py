import numpy as np
from Modules import BasicNetwork as BNet
import matplotlib.pyplot as plt
import pickle

from Utils import Local, Constants

confile_dir = Constants.LocalDataConstants.directories['n_confile_dir']

########################################################### Load Available Data ###########################################################

BehavioralData, Performance_data = Local.ExperimentDataLoader()
SOI = Local.AvailableSubjects()

################################################## Divide Subject into DEP and CTRL Groups ###########################################################

Sub_G = [[], []] # first element is CTRL Group Members and the Second one the DEP Group

for i, sub_i in enumerate(SOI[0]):

    if BehavioralData['BDI'][sub_i] < 10:

        Sub_G[0].append([i, sub_i])

    else:

        Sub_G[1].append([i, sub_i])

######################################################## Load Connectivity Data ######################################################
print("Enter Event Name: ")
event_name = input()
# event_name = 'Stim'
print("Enter Network of Interest")
NOI = input()
# NOI = 'ZeroAxis'
kernel = 'dPLI'
print("Enter Band Name: ")
Band = input()
# Band = 'Alpha'
print("Enter Group ID: ")
G_i = int(input())

Data = Local.HandleDataLoad(confile_dir + '\\' + event_name + '\\' + NOI + '\\' + kernel + '\\' + Band, version_number = 0)

##############################################

Data = [Data[str(SOI[1][sub_i[0]])] for sub_i in Sub_G[G_i]]
DataMean = (np.transpose(np.mean(np.array(Data), axis = 0), (0, 2, 3, 1)) - 0.5) * 5

print("Enter Block Number: ")
BlockNumber = int(input())
CNet = BNet.NetworkGraph(DataMean[BlockNumber])

CNet.SetCoords(Constants.LocalDataConstants.DefaulValues['NodeLocations'][NOI])
CNet.SetLabels(Constants.LocalDataConstants.names['NetworkNames'][NOI])

CNet.SetTimes(np.linspace(-0.1, 0.5, 150))

fig, ax = plt.subplots(1, 1, layout = 'constrained', figsize = (10, 10))

CNet.DrawDynamicGraph(VisThresh = 0.05, delay = 0.1, show_labels = True, xlims = Constants.LocalDataConstants.DefaulValues['xAxisLimits'][NOI], ylims = Constants.LocalDataConstants.DefaulValues['yAxisLimits'][NOI])
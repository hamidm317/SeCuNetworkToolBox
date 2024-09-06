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

event_name = 'Stim'
NOI = 'Frontal'
kernel = 'dPLI'
Band = 'Alpha'

Data = Local.HandleDataLoad(confile_dir + '\\' + event_name + '\\' + NOI + '\\' + kernel + '\\' + Band)

##############################################

Data_Ctrl = [Data[str(SOI[1][sub_i[0]])] for sub_i in Sub_G[0]]
CtrlDataMean = (np.transpose(np.mean(np.array(Data_Ctrl), axis = 0), (0, 2, 3, 1)) - 0.5) * 2 > 0.05

############################################################# Block 1 ####################################################################

CNetB1 = BNet.NetworkGraph(CtrlDataMean[0])

coords = [[0, 1], [-1, 0], [1, 0], [0, -1]]
CNetB1.SetCoords(coords)
CNetB1.SetLabels(['PF', 'LF', 'RF', 'MFC'])

CNetB1.SetTimes(np.linspace(-0.1, 0.5, 150))

fig, ax = plt.subplots(1, 1, layout = 'constrained', figsize = (10, 10))

# CNetB1.DrawStaticGraph(VisThresh = 0.5, win_number = 100, xlims = [-1.2, 1.2], ylims = [-1.2, 1.2], show_labels = True, ax = ax)

# plt.show()

CNetB1.DrawDynamicGraph(VisThresh = 0.05, delay = 0.1, show_labels = True)

############################################################# Block 2 ####################################################################

CNetB2 = BNet.NetworkGraph(CtrlDataMean[1])

coords = [[0, 1], [-1, 0], [1, 0], [0, -1]]
CNetB2.SetCoords(coords)
CNetB2.SetLabels(['PF', 'LF', 'RF', 'MFC'])

CNetB2.SetTimes(np.linspace(-0.1, 0.5, 150))

fig, ax = plt.subplots(1, 1, layout = 'constrained', figsize = (10, 10))

# CNetB1.DrawStaticGraph(VisThresh = 0.5, win_number = 100, xlims = [-1.2, 1.2], ylims = [-1.2, 1.2], show_labels = True, ax = ax)

# plt.show()

CNetB2.DrawDynamicGraph(VisThresh = 0.05, delay = 0.1, show_labels = True)
import numpy as np
from Modules import BasicNetwork as BNet
import pickle
from matplotlib.gridspec import GridSpec
import matplotlib.pyplot as plt
import scipy.stats as sps

from Utils import Local, Constants, SciPlot

########################################################## Define Constants #############################################################

confile_dir = Constants.LocalDataConstants.directories['n_confile_dir']
PlotSave_dir = Constants.LocalDataConstants.directories['plotSave_dir']

hist_axs = [1, 3, 5, 8, 10, 12]
trnd_axs = [2, 4, 6, 9, 11, 13]

pairs = [[1, 0], [2, 0], [2, 1], [3, 0], [3, 1], [3, 2]]
BlockLabel = ['Block 1', 'Block 2']

theta = np.pi / 4
phi = np.pi / 3

coords = [[np.cos(2 * theta + phi), np.sin(2 * theta + phi)], [np.cos(theta + phi), np.sin(theta + phi)], [np.cos(0 + phi), np.sin(0 + phi)], [np.cos(-1 * theta + phi), np.sin(-1 * theta + phi)]]

Bands = ['All', 'Delta', 'Theta', 'Alpha', 'Gamma', 'Beta']
NOIs = ['ZeroAxis', 'Frontal']
event_names = ['All', 'Stim']
kernel = 'dPLI'

VisThresh = 0.1

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

############################################################## Win Arrays ###########################################################################

win_step = 50
win_arrays = [[win, win + win_step] for win in np.arange(-100, 500, win_step)]

for event_name in event_names:

    for NOI in NOIs:

        for Band in Bands:

            Data = Local.HandleDataLoad(confile_dir + '\\' + event_name + '\\' + NOI + '\\' + kernel + '\\' + Band)

            Data_Ctrl = [Data[str(SOI[1][sub_i[0]])] for sub_i in Sub_G[0]]
            CtrlDataMean = (np.transpose(np.mean(np.array(Data_Ctrl), axis = 0), (0, 2, 3, 1)) - 0.5) * 5
            CtrlData = np.transpose(np.array(Data_Ctrl), (0, 1, 3, 4, 2))

            NetB = []

            for i in range(2):

                NetB.append(BNet.NetworkGraph(CtrlDataMean[i]))

            for NetBB in NetB:

                NetBB.SetCoords(coords)
                NetBB.SetLabels(Constants.LocalDataConstants.names['NetworkNames'][NOI])

            for win_array in win_arrays:

                STP, FTP = Local.TimeToSample(win_array)
                fig = plt.figure(figsize = (15, 12), layout = 'constrained', dpi = 500)
                gs = GridSpec(6, 5, figure = fig)

                axs = []

                axs.append(fig.add_subplot(gs[:3, 1:4]))

                axs.append(fig.add_subplot(gs[0, 0]))
                axs.append(fig.add_subplot(gs[0, 4]))

                axs.append(fig.add_subplot(gs[1, 0]))
                axs.append(fig.add_subplot(gs[1, 4]))

                axs.append(fig.add_subplot(gs[2, 0]))
                axs.append(fig.add_subplot(gs[2, 4]))

                axs.append(fig.add_subplot(gs[3:, 1:4]))

                axs.append(fig.add_subplot(gs[3, 0]))
                axs.append(fig.add_subplot(gs[3, 4]))

                axs.append(fig.add_subplot(gs[4, 0]))
                axs.append(fig.add_subplot(gs[4, 4]))

                axs.append(fig.add_subplot(gs[5, 0]))
                axs.append(fig.add_subplot(gs[5, 4]))

                for Bi, NetBB in enumerate(NetB):

                    NetBB.DrawStaticGraph(VisThresh = VisThresh, window = win_array, xlims = [-1, 1], ylims = [0.2, 1], show_labels = True, ax = axs[Bi * 7], DirectionBias = 0)
                    axs[Bi * 7].set_title(BlockLabel[Bi])

                    for i in range(6):

                        axs[hist_axs[i]].hist(np.mean(CtrlData[:, Bi, :, :, STP : FTP], axis = 3)[:, pairs[i][0], pairs[i][1]], alpha = 0.5, label = BlockLabel[Bi])
                        axs[hist_axs[i]].set_xlim([0, 1])
                        axs[hist_axs[i]].set_title(Constants.LocalDataConstants.names['JulyClusterNames'][Constants.LocalDataConstants.NetworksOfInterest[NOI][pairs[i][0]]] + ' - ' + Constants.LocalDataConstants.names['JulyClusterNames'][Constants.LocalDataConstants.NetworksOfInterest[NOI][pairs[i][1]]], fontsize = 10)
                        axs[hist_axs[i]].legend()


                for i in range(6):

                    Data2Trnd = np.mean(CtrlData[:, :, pairs[i][0], pairs[i][1], STP : FTP], axis = -1)
                    pVal = sps.ttest_ind(Data2Trnd[:, 0], Data2Trnd[:, 1]).pvalue
                    y_U, y_L = SciPlot.ConfidenceBoundsGen(Data2Trnd)
                    axs[trnd_axs[i]].plot(np.mean(Data2Trnd, axis = 0))
                    axs[trnd_axs[i]].fill_between(np.arange(2), y_U, y_L, alpha = 0.2)
                    axs[trnd_axs[i]].set_title(Constants.LocalDataConstants.names['JulyClusterNames'][Constants.LocalDataConstants.NetworksOfInterest[NOI][pairs[i][0]]] + ' - ' + Constants.LocalDataConstants.names['JulyClusterNames'][Constants.LocalDataConstants.NetworksOfInterest[NOI][pairs[i][1]]] + ' (p-Value = ' + str(int(10000 * pVal / 2) / 10000) + ' )', fontsize = 10)
                    axs[trnd_axs[i]].set_xlim([0, 1])

                fig.suptitle(NOI + ' Network During Learning in Control Subjects in Band ' + Band + ' (dPLI) Locked on ' + event_name + ' Onset\nTime windows ' + str(win_array[0]) + 'ms to ' + str(win_array[1]) + 'ms', fontsize = 15)

                SavePlotsLoc = Local.HandleDir(PlotSave_dir + '\\' + event_name + '\\NetworkAnalyses\\' + NOI + '\\' + kernel + '\\' + Band)
                fig.savefig(SavePlotsLoc + '\\' + 'ControlGroup_LockedOn_' + event_name + '_' + str(win_array[0]) + 'msTo' + str(win_array[1]) + 'ms')
                plt.close()

                print('Figure Saved')
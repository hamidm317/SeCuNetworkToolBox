import numpy as np

class FigConstants:

    StaticGraph = {

        'figsize': (5, 5),
        'edgesize': 15,
        'labelsize': 10,
        'ArrowHeadWidth': 0.05,
        'ArrowBodyWidth': 0.001,
        'ArrowHeadLength': 0.1

    }

class LocalDataConstants():

    directories = {

        'eeg_file_dir': r'E:\HWs\Msc\Research\Research\Depression Dataset\New Datasets\Clustered_SingleTrialData_All_Neg_Pos_Stim.mat',
        'beh_dir_file': r'E:\HWs\Msc\Research\Research\Depression Dataset\depression_rl_eeg\Depression PS Task\Scripts from Manuscript\Data_4_Import.xlsx',
        'perform_data_dir': r'E:\HWs\Msc\Research\Research\Depression Dataset\New Datasets\Subjects_Behavioral_datas.csv',
        'eeg_prep_datasets_dir': r'E:\\HWs\Msc\\Research\\Research\\Depression Dataset\\Testing Preprocess',
        'confile_dir': r'D:\AIRLab_Research\Data\ConnectivityDataDict.pickle',
        'n_confile_dir': r'D:\AIRLab_Research\Data',
        'plotSave_dir': r'D:\AIRLab_Research\Plots',
        'ListOfAvailableSubjects': r'D:\AIRLab_Research\Data\BehavioralData\AvailableSubjects.npy',
        'fd_excel_dir': r'D:\AIRLab_Research\Features\FeatureDraft.xlsx'
    }

    names = {

        'JulyClusterNames': ['PF', 'LF', 'RF', 'MFC', 'LT', 'RT', 'LFC', 'RFC', 'MPC', 'LPC', 'RPC', 'MP', 'LPO', 'RPO'],
        'freq_bands': ['Delta', 'Theta', 'Alpha', 'Beta', 'Gamma', 'LowBeta', 'HighBeta', 'LowGamma', 'MidGamma', 'HighGamma', 'All'],
        'events': ['All', 'Neg', 'Pos', 'Stim'],
        'LocalCM':{

            'Transfer Entropy': 'TE',
            'PLI': 'PLI',
            'Granger Causality': 'LRB_GC',
            'dPLI': 'dPLI',
            'wPLI': 'wPLI',
            'PLV': 'PLV',

            'Stimulus': 'Stim',
            'Stim': 'Stim',
            'PosNeg': 'PosNeg',
            'Feedback': 'All',
            'Action': 'Action',
            'All': 'All'
        },

        'NetworkNames':{

            'ZeroAxis': ['PF', 'MFC', 'MPC', 'MP'],
            'Frontal': ['PF', 'LF', 'RF', 'MFC']

        }
    }

    NetworksOfInterest = {

        'All': np.arange(14),
        'ZeroAxis': [0, 3, 8, 11],
        'Frontal': [0, 1, 2, 3],
        'OcciTemporal': [4, 5, 12, 13]

    }

    Labels = {

        'groups': ['Control', 'Depressed'],
        'data_block': ['Block 1', 'Block 2']
    }

    DefaulValues = {

        'overlap_ratio': 0.98,
        'window_length': 100,
        'trial_in_block': 10, # -> In Stim Locked Analyses
        'min_trial': 20, # -> In PosNeg Locked Analyses

        'Circuit':{

            'ZeroPoint': 25,
            'Fs': 250
        },

        'Univariate':{

            'ZeroPoint': 100,
            'Fs': 500
        },

        'NodeLocations':{

            'ZeroAxis': [[np.cos(2 * np.pi / 4 + np.pi / 3), np.sin(2 * np.pi / 4 + np.pi / 3)], [np.cos(np.pi / 4 + np.pi / 3), np.sin(np.pi / 4 + np.pi / 3)], [np.cos(0 + np.pi / 3), np.sin(0 + np.pi / 3)], [np.cos(-1 * np.pi / 4 + np.pi / 3), np.sin(-1 * np.pi / 4 + np.pi / 3)]],
            'Frontal': [[0, 1], [-1, 0], [1, 0], [0, -1]]

        },

        'xAxisLimits':{

            'ZeroAxis': [-1.2, 1.2],
            'Frontal': [-1.2, 1.2]
        },

        'yAxisLimits':{

            'ZeroAxis': [0.2, 1],
            'Frontal': [-1.2, 1.2]
        }

    }

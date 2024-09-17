import numpy as np

def ConfidenceBoundsGen(Data, Confidence_Level = 1.96):

    assert Data.ndim < 3 and Data.ndim > 0, "Data must be vector or 2 way matrix"

    if Data.ndim == 2:

        y_Upper = []
        y_Lower = []

        [num_samples, num_timePoint] = Data.shape

        for t_p in range(num_timePoint):

            U_tmp, L_tmp = ConfidenceBound(Data[:, t_p], Confidence_Level)

            y_Upper.append(L_tmp)
            y_Lower.append(U_tmp)

        return np.array(y_Upper), np.array(y_Lower)
    
    else:

        return 0
    
def ConfidenceBound(Data, Confidence_Level):

    UB_CI = np.mean(Data) + Confidence_Level * np.std(Data) / np.sqrt(len(Data))
    LB_CI = np.mean(Data) - Confidence_Level * np.std(Data) / np.sqrt(len(Data))

    return UB_CI, LB_CI

def AestDim(Q, thr = 3):

    CanDims_t = []

    for i in range(1, int(Q / 2) + 1):

        if np.mod(Q, i) == 0:

            CanDims_t.append([i, int(Q / i)])

    BestDims = CanDims_t[-1]

    if max([BestDims[0] / BestDims[1], BestDims[1] / BestDims[0]]) <= thr:

        return np.sort(CanDims_t[-1])
    
    else:
        
        return AestDim(Q + 1)
    
def MovMean(A, k):

    win_length = k
    MAFA = []
    
    if len(A) < k:

        print("I don't know how to calculate this, The window must be less than length. So the length forced to be len(A)")

        win_length = len(A)

    new_elements_len = len(A) - win_length + 1

    for element in range(new_elements_len):

        MAFA.append(np.mean(A[element : (element + 1) + k ]))

    return np.array(MAFA)

def RandomBlockSampling(Length: int, NumBlock: int, NumSample_inBlock: int):

    Block_Len = int(Length / NumBlock)

    # assert NumSample_inBlock <= Block_Len, 'Number of Samples in Blocks must be less than length of Block'

    if  NumSample_inBlock >= Block_Len:

        NumSample_inBlock = Block_Len

    SampleMat = []

    for Block in range(NumBlock - 1):

        SampleMat.append(np.random.permutation(Block_Len)[:NumSample_inBlock] + Block * Block_Len)

    SampleMat.append(Length - 1 - np.random.permutation(Block_Len)[:NumSample_inBlock])

    return np.array(SampleMat)

def DeterminedBlockSampling(Length: int, NumBlock: int, NumSample_inBlock: int):

    Block_Len = int(Length / NumBlock)

    # assert NumSample_inBlock <= Block_Len, 'Number of Samples in Blocks must be less than length of Block'

    if  NumSample_inBlock >= Block_Len:

        NumSample_inBlock = Block_Len

    SampleMat = []

    for Block in range(NumBlock - 1):

        SampleMat.append(np.int32(np.arange(NumSample_inBlock)) + Block * Block_Len)

    SampleMat.append(Length - 1 - np.int32(np.arange(NumSample_inBlock)))

    return np.array(SampleMat)
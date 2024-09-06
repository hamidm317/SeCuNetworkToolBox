import numpy as np

def NetBasixByWeMat(WeMat):

    assert WeMat.shape[0] == WeMat.shape[1], "Weights must be square Matrix!"

    Static = True

    if WeMat.ndim == 3:

        if WeMat.shape[2] > 1:

            Static = False

    else:

        WeMat = np.reshape(WeMat, WeMat.shape + (1, ))

    Directed = isDirected(WeMat)
    Weighted = isWeighted(WeMat)

    if not Weighted:

        WeMat = PrepBinaryNetwork(WeMat)

    return WeMat, Static, Directed, Weighted

def PrepBinaryNetwork(WeMat):

    UnVals = np.sort(np.unique(WeMat))

    for UV_i, UnVal in enumerate(UnVals):

        WeMat[np.where(WeMat == UnVal)] == int(UV_i)

    return WeMat

def isDirected(WeMat):

    for time_i in range(WeMat.shape[2]):

        tWeMat = WeMat[:, :, time_i]

        if not np.all(tWeMat == tWeMat.T):

            return True

    return False

def isWeighted(WeMat):

    if not len(np.unique(WeMat)) == 2:

        return True

    else:

        return False
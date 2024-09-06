import numpy as np
import matplotlib.pyplot as plt
import time

import Utils.GraphMeasures as GrM
from Utils.Constants import FigConstants
    
class NetworkGraph:

    # WeMat (Weight Matrix) must be NxNxTimeWindow (N: number of nodes)

    def __init__(self, w_mat):

        self.weights, self.Static, self.Directed, self.Weighted = GrM.NetBasixByWeMat(w_mat)

    def SetCoords(self, coords = None): # it must be possible to define other forms of node coordinations

        if np.any(coords == None):

            coords = np.random.uniform(low = -1, high = 1, size = (self.weights.shape[1], 2))
        
        assert len(coords) == self.weights.shape[1], 'Coordinations must be available for each Node'

        self.coords = np.array(coords)

    def SetTimes(self, times):

        assert self.weights.shape[2] == len(times), 'time vector must has same length as number of temporal evolving matrices'

        self.t_ = times

    def SetLabels(self, labels):

        assert self.weights.shape[1] == len(labels), "Label numbers must be equal to number of nodes"

        self.labels = labels

    def DrawStaticGraph(self, VisThresh: int, win_number = 0, ax = None, show_labels = False, xlims = [-1, 1], ylims = [-1, 1]):

        # ISSUES: 
        # - isn't better way to plot DIRECTED graphs? (:|)

        # Draws a time sample,
        # win_number -> number of intended window
        # VisThresh -> Threshold to Consider Edge (it is useful to increase the sparsity of graph)

        if ax == None:

            fig, ax = plt.subplots(1, 1, layout = 'constrained', figsize = FigConstants.StaticGraph['figsize'], dpi = 200)

        x = self.coords[:, 0]
        y = self.coords[:, 1]

        if not self.Directed:

            for i in range(len(x)):

                for j in range(i + 1, len(x)):

                    color_num = self.weights[i, j, win_number]

                    if color_num < 0:

                        color_num = 0

                    elif color_num > 1:

                        color_num = 1

                    if color_num > VisThresh:

                        ax.plot([x[i], x[j]], [y[i], y[j]], color = str(1 - color_num))

        else:

            for i in range(len(x)):

                for j in range(len(x)):

                    if i != j:

                        color_num = self.weights[i, j, win_number]

                        if color_num < 0:

                            color_num = 0

                        elif color_num > 1:

                            color_num = 1

                        if color_num > VisThresh:

                            bias = 0.5 * FigConstants.StaticGraph['ArrowHeadWidth']

                            if x[j] == x[i]:

                                if y[j] > y[i]:

                                    delta = np.pi / 2

                                else:

                                    delta = -1 * np.pi / 2

                            else:

                                delta = np.arctan((y[j] - y[i]) / (x[j] - x[i]))

                            cos = np.cos(delta) * np.sign(j - i)
                            sin = np.sin(delta)

                            cbias = bias * cos
                            sbias = bias * -1 * sin

                            ax.arrow(x[i] + sbias, y[i] + cbias, x[j] - x[i], y[j] - y[i], color = str(1 - color_num),
                            head_width = FigConstants.StaticGraph['ArrowHeadWidth'], width = FigConstants.StaticGraph['ArrowBodyWidth'],
                            length_includes_head = True,
                            head_length = FigConstants.StaticGraph['ArrowHeadLength'])

        for i in range(len(x)):

            ax.plot(x[i], y[i], marker="o", markersize = FigConstants.StaticGraph['edgesize'], markeredgecolor="red", markerfacecolor="green")

            if show_labels:

                ax.text(x[i], y[i], str(self.labels[i]), fontsize = FigConstants.StaticGraph['labelsize'], horizontalalignment = 'center', verticalalignment = 'center')

        ax.axis(False)
        ax.set_xlim(xlims)
        ax.set_ylim(ylims)

    def DrawDynamicGraph(self, delay: int, VisThresh = 0.5, xlims = [-1.2, 1.2], ylims = [-1.2, 1.2], show_labels = False):

        plt.ion()
        
        fig, ax = plt.subplots(1, 1, figsize = FigConstants.StaticGraph['figsize'])

        for i in range(self.weights.shape[2]):

            fig.canvas.draw()
            ax.set_title("Window time: " + str(np.floor(self.t_[i] * 100) / 100))
            self.DrawStaticGraph(VisThresh = VisThresh, win_number = i, ax = ax, xlims = xlims, ylims = ylims, show_labels = show_labels)
            time.sleep(delay)
            fig.canvas.flush_events()
            ax.clear()
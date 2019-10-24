import numpy as np
from matplotlib import pyplot as plt
from numpy import random

from utils.PlotEllipse import PlotEllipse

isempty = lambda a: np.all(a==0)

class MapCanvas:
    """For use in practice 6"""
    def __init__(self, nFeatures):
        # MATPLOTLIB
        self.fig, self.ax = plt.subplots()
        self.ax.set_xlim([-70, 70])
        self.ax.set_ylim([-70, 70])
        plt.grid()
        plt.tight_layout()
        np.set_printoptions(precision=3)

        self.fig.canvas.draw()

        # Number of readings
        self._reading = []
        self._observed_times = np.zeros((nFeatures, 2), dtype=object)
        
        # Map graphics
        self.k = 0
        self.handler_ellipse = []
        self.handler_state = []
        
    def increment_observed_times(self, iFeature):
        self._observed_times[iFeature,0] = self._observed_times[iFeature,0]+1
        
    def PlotNumberOfReadings(self, xVehicleTrue, iFeature, Map):
        
        for c in range(len(self._reading)):
            if (self._reading[c] is not None):
                self._reading[c].pop(0).remove()

        self._reading=np.zeros(len(iFeature), dtype=object)

        if (self._observed_times[iFeature[0],1]!=0):
            self._observed_times[iFeature[0],1].remove()

        # ... #TODO Lookup https://www.mathworks.com/help/matlab/ref/text.html
        self._observed_times[iFeature[0], 1] = self.ax.text(
            x = Map[0, iFeature[0]]+random.rand(),
            y = Map[1, iFeature[0]]+random.rand(),
            s = '{}'.format(self._observed_times[iFeature[0], 0])
        )

        for c in range(len(iFeature)):
            if (iFeature[c] != -1):
                self._reading[c] = self.ax.plot(
                    [xVehicleTrue[0], Map[0, iFeature[c]]], 
                    [xVehicleTrue[1], Map[1, iFeature[c]]]
                )
            else:
                self._reading[c] = None
        self.fig.canvas.draw()

    def DoMapGraphics(self, robot, nSigma=5):

        if(isempty(self.k)):
            self.k = 0
        
        self.k += 1
        # removing ellipses from the previous iteration
        if isempty(self.handler_ellipse):
            self.handler_ellipse=np.zeros(len(robot.xEst),1)
        else:
            for i in range(len(self.handler_ellipse)):
                if (self.handler_ellipse[i]!=0):
                    # Remove from plot uses h.pop(0).remove()
                    self.handler_ellipse[i].pop(0).remove()
                    self.handler_ellipse[i] = 0

                #end
            #end

        # removing state from the previous iteration
        if (isempty(self.handler_state)):
            self.handler_state = np.zeros(len(robot.xEst))
        else:
            for i in range(len(self.handler_state)):
                if (self.handler_state[i]!=0):
                    self.handler_state[i].pop(0).remove()
                    self.handler_state[i]=0
                #end
            #end
        #end

        self.handler_ellipse = np.zeros(len(robot.xEst),object)
        self.handler_state = np.zeros(len(robot.xEst),object)
        colors = 'rbyg'
        for i in range(round(robot.xEst.size/2)):
            iL = 2*i
            iH = 2*i+2
            x = robot.xEst[iL:iH]
            P = robot.PEst[iL:iH,iL:iH]
            c = colors[i % 4]
            #set(handler_ellipse(i),'color',chr(c))
            self.handler_ellipse[i]= PlotEllipse(self.fig, self.ax, x, P, nSigma, color=c)
            self.handler_state[i]= self.ax.plot(x[0,0],x[1,0],'.',color=c)
            # plot3(x(1),x(2),k,'r+')
        #end
        self.fig.canvas.draw()
    #end
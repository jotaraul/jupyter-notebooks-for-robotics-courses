import numpy as np
from matplotlib import pyplot as plt
from numpy import random

from utils.PlotEllipse import PlotEllipse
from utils.DrawRobot import DrawRobot

isempty = lambda a: np.all(a==0)

class MapCanvas:
    """For use in practice 7"""
    def __init__(self, Map, MapSize, nFeatures, robot, sensor, NONSTOP):
        self.NONSTOP = NONSTOP
        self.n_features = nFeatures
        self.MapSize = MapSize
        self.hObsLine = None
        self.hFOV = None
        
        # Drawings
        self.fig, self.ax = plt.subplots()
        #plt.ion()
        plt.axis([-MapSize/2-40, MapSize/2+40, -MapSize/2-40, MapSize/2+40])
        plt.grid()
        plt.tight_layout()
        
        self.colors = np.zeros((nFeatures,3))
        for i_feat in range(nFeatures):
            self.colors[i_feat,:] = [random.rand(), random.rand(), random.rand()]
        
    def initialFrame(self, robot, Map, sensor):
        
        for i_feat in range(self.n_features):
            self.ax.plot(
                Map[0,i_feat],
                Map[1,i_feat],
                's',
                color=self.colors[i_feat,:],
                #MarkerFaceColor=colors[i_feat,:],
                MarkerSize=10)

        self.hObsLine = self.ax.plot([0,0],[0,0], linestyle=':')
        robot.draw(self.fig, self.ax)
        self.hFOV = sensor.drawFOV(self.fig, self.ax, robot.true_pose,'b')

        self.fig.canvas.draw() # flush pending drawings events
        if(not self.NONSTOP):
            plt.waitforbuttonpress(-1)

        self.hFOV.pop(0).remove()

    def drawFrame(self, robot, sensor, Map, iFeature):
        # Robot estimated, real, and ideal poses, fov and uncertainty
        if iFeature >= 0:
            self.hObsLine = sensor.drawLines(self.fig, self.ax, robot.true_pose, Map[:, [iFeature]])
        
        self.hEllipses = robot.draw(self.fig, self.ax)
        self.hFOV = sensor.drawFOV(self.fig, self.ax, robot.true_pose,'b')
        
        self.fig.canvas.draw() # flush pending drawings events
        if(not self.NONSTOP):
            plt.waitforbuttonpress(-1)
        else:
            plt.pause(0.1)
        #Clean a bit
        self.hFOV.pop(0).remove()
        
        for i in range(len(self.hEllipses)):
            self.hEllipses[i].pop(0).remove()
        
    def drawFinal(self, robot):
        # Draw the final estimated positions and uncertainties of the features
        plt.axis([-self.MapSize/2-40, self.MapSize/2+40, -self.MapSize/2-40, self.MapSize/2+40])
        robot.draw(self.fig, self.ax, final=True)
        self.fig.canvas.draw() # flush pending drawings events
        if(not self.NONSTOP):
            self.fig.canvas.draw() # flush pending drawings events
            plt.waitforbuttonpress(-1)

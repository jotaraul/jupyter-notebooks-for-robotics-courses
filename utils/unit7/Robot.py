import numpy as np
from numpy import random

from utils.tcomp import tcomp
from utils.DrawRobot import DrawRobot
from utils.PlotEllipse import PlotEllipse


class EFKSlamRobot():
    def __init__(self, true_pose, cov_move, n_features):
        # Robot description
        self.pose = true_pose
        self.true_pose = true_pose
        self.cov_move = cov_move

        # State -- Initially only pose, no map
        self.xEst = true_pose
        self.PEst = np.zeros((3, 3))
        self.MappedFeatures = -1*np.ones((n_features,2), int)

    def step(self, u):
        self.pose = tcomp(self.pose,u) # New pose without noise

        noise = np.sqrt(self.cov_move)@random.randn(3,1) # Generate noise
        noisy_u = tcomp(u, noise) # Apply noise to the control action
        self.true_pose = tcomp(self.true_pose,noisy_u)
    
    def draw(self, fig, ax, Map=[], final=False):
        DrawRobot(fig, ax, self.xEst[0:3], color='g')
        DrawRobot(fig, ax, self.true_pose, color='b')
        DrawRobot(fig, ax, self.pose, color='r')

        PlotEllipse(fig, ax, self.xEst[0:3], self.PEst[0:3, 0:3], 5, color='g', linewidth=.5)

        # The uncertainty of each perceived landmark
        n = len(self.xEst)
        nF = int((n-3)/2)
        hEllipses = []
        for i in range(nF):
            iF = 3+2*i
            if final:
                ax.plot(self.xEst[iF], self.xEst[iF+1], 'gs')
            else:
                ax.plot(self.xEst[iF], self.xEst[iF+1], 'b*')
            hEllipse = PlotEllipse(fig, ax, self.xEst[iF:iF+2], self.PEst[iF:iF+2,iF:iF+2], 3, color='r', linewidth=1)
            hEllipses.append(hEllipse)
        
        return hEllipses
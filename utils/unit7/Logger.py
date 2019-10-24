import numpy as np
from matplotlib import pyplot as plt
from scipy import linalg

class Logger():
    def __init__(self, nFeatures, nSteps):
        # Storage:
        self.PFeatDetStore = np.full((nFeatures,nSteps),np.Inf)
        self.FeatErrStore = np.full((nFeatures,nSteps),np.Inf)
        self.PXErrStore = np.full((nSteps,1), 0)
        self.XErrStore = np.full((2,nSteps), 0) # error in position and angle
        
    def log(self, robot, Map, k):
        # TODO
        IsMapped = robot.MappedFeatures[:,0] >= 0
        # Storage:
        for i in range(robot.MappedFeatures.shape[0]):
            if IsMapped[i]:
                ii = robot.MappedFeatures[i,:]
                xFeature = robot.xEst[ii[0]:ii[1]]
                self.PFeatDetStore[i,k] = np.linalg.det(robot.PEst[ii[0]:ii[1],ii[0]:ii[1]])
                self.FeatErrStore[i,k] = np.sqrt(np.sum((xFeature-Map[:,[i]])**2))
        self.PXErrStore[k,0] = linalg.det(robot.PEst[0:3,0:3])
        self.XErrStore[0,k] = np.sqrt(np.sum((robot.xEst[0:2]-robot.true_pose[0:2])**2))  # error in position and angle
        self.XErrStore[1,k] = abs(robot.xEst[2]-robot.true_pose[2])  # error in position and angle
        
    def draw(self, colors):
        nSteps = self.PFeatDetStore.shape[1]
        nFeatures = self.PFeatDetStore.shape[0]
        
        plt.figure(2) #hold on
        plt.title('Errors in robot localization')
        plt.plot(self.XErrStore[0,:],'b',label="Error in position")
        plt.plot(self.XErrStore[1,:],'r',label="Error in orientation")
        #plt.legend('Error in position','Error in orientation')
        plt.legend()

        plt.figure(3)# hold on
        plt.title('Determinant of the cov. matrix associated to the robot localization')
        xs = np.arange(nSteps)
        plt.plot(self.PXErrStore[:],'b')

        plt.figure(4)# hold on
        plt.title('Errors in features localization')

        plt.figure(5)# hold on
        plt.title('Log of the determinant of the cov. matrix associated to each feature')

        for i in range(nFeatures):
            plt.figure(5)
            h = plt.plot(np.log(self.PFeatDetStore[i,:]), color=colors[i,:])
            plt.figure(4)
            h = plt.plot(self.FeatErrStore[i,:], color=colors[i,:])

            
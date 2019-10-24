import numpy as np
from numpy.linalg import eig
from scipy.linalg import sqrtm
import matplotlib.pyplot as plt

from utils.tcomp import tcomp

def DrawRobot(fig, ax, pose, axis_percent=0.02, color='red', linewidth=.5, **kwargs):
# This function draws a triangle representing a robot at pose Xr (x,y,theta, using the color 'col' 
# This code has been taken/adapted from  P. Newman http://www.robots.ox.ac.uk/~pnewman
    axis_percent=0.02 # percentage of axes size 
    a=plt.axis()
    l1=axis_percent*(a[1]-a[0])
    l2=axis_percent*(a[3]-a[2])
    P=np.array([[-1,1,0,-1],[-1,-1, 3,-1]])#basic triangle
    theta = pose[2, 0]-np.pi/2#rotate to point along x axis (theta = 0)
    c=np.cos(theta)
    s=np.sin(theta)
    P=np.array([[c,-s],[s, c]])@P #rotate by theta
    P[0,:]=P[0,:]*l1+pose[0, 0] #scale and shift to x
    P[1,:]=P[1,:]*l2+pose[1, 0]
    h = ax.plot(P[0,:],P[1,:], color=color, linewidth=linewidth, **kwargs)# draw
    #hold on,
    ax.plot(pose[0, 0],pose[1, 0],'+',color=color, markersize=(3*linewidth +1), linewidth=linewidth)
    
    return h

def PlotEllipse(fig, ax, mean, cov, scale=1, **kwargs):
    """This function draws a ellipse representing a Gaussian centered at x (mean) and with covariance P 
        This code has been adapted from the file DoVehicleGraphics.m by P.# Newman http://www.robots.ox.ac.uk/~pnewman
    
        Arguments:
        mean -- the center of the ellipse (i.e. the mean of the distribution) 
        cov -- the covariance matrix, of any dimension, but only the upper 2-by-2 submatrix is considered
        scale -- number of sigma we want to plot (scale factor). Default: 1
        **kwargs -- every remaining named parameter is passed to plt.plot(). We can pass 'color', 'linewidth' among others.
    """
    
    mean = mean[0:2]
    cov = cov[0:2,0:2]                      # only plot x-y part
    
    if(not np.any(np.diag(cov)==0)):
        D,V = eig(cov)                      #V: eigenvectors, D: eigenvalues
        
        y = (
            scale*
            np.vstack(
                (np.cos(np.arange(0.,(2*np.pi),0.1)),
                np.sin(np.arange(0.,(2*np.pi),0.1)))
                ))                          #Points of a circunference o radius nSigma
        
        axes = V@sqrtm(np.diag(D))          # Axes of the ellipse, 2-by-2 matrix
        el = axes@y                         # Points of the ellipse
        ei = np.vstack(el[:,0])
        el = np.concatenate((el,ei),axis=1) # To close the ellipse
        el += np.tile(mean,(1,el.shape[1])) # To translate it according to the robot pose
        
        res = ax.plot(el[0,:],el[1,:], **kwargs) #creates a line object and plot the ellipse
        return res

def drawObservations(fig, ax, from_pose, world, linestyle=':', **kwargs):
    for i in range(world.shape[1]):
        if i >=0:
            ax.plot(
                [from_pose[0, 0], world[0, i]],
                [from_pose[1, 0], world[1, i]],
                linestyle=linestyle,
                **kwargs
        )


def drawFOV(fig, ax, from_pose, fov, max_range, color='b', linewidth=.5, **kwargs):
    alpha = fov/2
    angles = np.linspace(-alpha,alpha, (fov/0.01))
    nAngles = angles.shape[0]
    arc_points = np.zeros((2,nAngles))

    for i in range(nAngles):
        u = np.vstack([
            max_range*np.cos(angles[i]),
            max_range*np.sin(angles[i]),
            1
        ])
        aux_point = tcomp(from_pose,u)
        arc_points[0,i] = aux_point[0,0]
        arc_points[1,i] = aux_point[1,0]

    h = ax.plot(
            np.hstack((from_pose[0,0], arc_points[0], from_pose[0,0])),
            np.hstack((from_pose[1,0], arc_points[1], from_pose[1,0])),
            color=color,
            linewidth=linewidth,
            **kwargs
        )

    return h
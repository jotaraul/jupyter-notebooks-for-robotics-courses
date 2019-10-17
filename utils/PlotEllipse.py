# This function draws a ellipse representing a Gaussian centered at x (mean) and with covariance P 
# This code has been adapted from the file DoVehicleGraphics.m by P.# Newman http://www.robots.ox.ac.uk/~pnewman

import numpy as np
from numpy.linalg import eig
from scipy.linalg import sqrtm
from matplotlib import patches
import matplotlib.pyplot as plt

def pltEllipse(fig, ax, mean, cov, scale=1, linewidth=.5, fill=False, **kwargs):
    mean = mean[0:2]
    cov = cov[0:2,0:2]                      # only plot x-y part
    
    if(not np.any(np.diag(cov)==0)):
        D,V = eig(cov)                      #V: eigenvectors, D: eigenvalues
        axes = V@sqrtm(np.diag(D))          # Axes of the ellipse, 2-by-2 matrix

        width = 2*scale*abs(axes[0,0]- axes[1,0])
        height = 2*scale*abs(axes[0,1]- axes[1,1])
        angle = np.arctan2(axes[1,0], axes[0,0])*180/np.pi
        h = ax.add_patch(patches.Ellipse((mean[0,0], mean[1,0]), 
                                       width, 
                                       height, 
                                       angle,
                                       linewidth=linewidth,
                                       fill=fill,
                                       **kwargs))
        return h

def PlotEllipse(fig, ax,mean, cov, scale=1, **kwargs):
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


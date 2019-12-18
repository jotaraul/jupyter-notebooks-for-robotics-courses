import numpy as np
from numpy import random
from matplotlib import pyplot as plt

from utils.AngleWrap import AngleWrapList
from utils.tcomp import tcomp
from utils.Drawings import drawObservations, drawFOV

class FOVSensor():
    def __init__(self, cov_sensor, fov, max_range):
        self.fov = fov
        self.max_range = max_range
        self.cov_sensor = cov_sensor

    def observe(self, from_pose, world, noisy=True, flatten=True):
        delta = world - from_pose[0:2]

        # Observation model
        z = np.empty((2, world.shape[1]))
        z[0, :] = np.sqrt(np.sum(delta**2, axis=0))
        z[1, :] = np.arctan2(delta[1, :], delta[0, :]) - from_pose[2, 0]
        z[1, :] = AngleWrapList(z[1, :])

        # Add noise if neccesary
        if noisy: 
            z += np.sqrt(self.cov_sensor)@random.randn(2, world.shape[1])

        # Flatten into a vertical vector if neccesary
        if flatten:
            return np.vstack(z.flatten('F'))
        else:
            return z

    def random_observation(self, from_pose, world, noisy=True, fov=True):
        # GLobal observation or only in fov
        if fov:
            z, feats_idx = self.observe_in_fov(from_pose, world, noisy=noisy, flatten=False)
        else:
            z = self.observe(from_pose, world, noisy=noisy, flatten=False)

        # Select random landmark
        n_landmarks = z.shape[1]
        if n_landmarks > 0:
            rand_idx = random.randint(n_landmarks)

            z = z[:, [rand_idx]]
            if fov:
                rand_idx = feats_idx[rand_idx]

            return z, rand_idx
        else:
            return z, -1

    def observe_in_fov(self, from_pose, world, noisy=True, flatten=True):
        ang_lim = self.fov/2

        # Normal observation
        z = self.observe(from_pose, world, noisy=noisy, flatten=False)

        # Filter results in fov
        feats_idx = np.where(
            (np.abs(z[1, :]) < ang_lim) & 
            (z[0, :] < self.max_range)
        )[0]
        z = z[:, feats_idx]
        
        # Flatten if necessary
        if flatten and z.size>0:
            z = np.vstack(z.flatten('F'))
        
        return z, feats_idx

    def drawFOV(self, fig, ax, from_pose, color='b', linewidth=.5, **kwargs):
        return drawFOV(fig, ax,
                       from_pose, self.fov,
                       self.max_range, color=color,
                       linewidth=linewidth, **kwargs)
    
    def drawLines(self, fig, ax, from_pose, world, linestyle=':', **kwargs):
        return drawObservations(fig, ax,
                                from_pose, world,
                                linestyle=linestyle, **kwargs)
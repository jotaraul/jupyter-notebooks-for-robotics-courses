from numpy import array, sin, cos, pi
import numpy as np
from utils.AngleWrap import AngleWrap

def tcomp(tab,tbc):
    '''
    Composition of transformations given by poses
    '''
    if (tab.shape[0] != 3):
        raise Exception('TCOMP: tab is not a valid transformation!')
    if (tbc.shape[0] != 3):
        raise Exception('TCOMP: tbc is not a valid transformation!')

    ang = tab[2, 0]+tbc[2, 0]
    
    if ang > pi or ang <= -pi:
        ang = AngleWrap(ang)

    s = sin(tab[2, 0])
    c = cos(tab[2, 0])
    tac = np.vstack((
        tab[0:2] + array([[c, -s],[s, c]]) @ tbc[0:2],
        ang
        ))
   
    return tac
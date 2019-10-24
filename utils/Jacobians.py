from numpy import vstack, sin, cos

def J1(x1,x2):
    s1 = sin(x1[2, 0])
    c1 = cos(x1[2, 0])
    return vstack((
            [1, 0,  -x2[0,0]*s1-x2[1,0]*c1],
            [0, 1,  x2[0,0]*c1-x2[1,0]*s1],
            [0, 0, 1]
            ))

def J2(x1,x2):
    s1 = sin(x1[2, 0])
    c1 = cos(x1[2, 0])
    return vstack((
            [c1,-s1,0],
            [s1,c1,0],
            [0 , 0, 1]
            ))

def Jab(tab):
    if (tab.shape[0] != 3):
        raise Exception('J tab is not a transformation!!!')
    s = sin(tab[2,0])
    c = cos(tab[2,0])
    return vstack((
        [c,-s, tab[1,0]],
        [s,c,-tab[0,0]],
        [0, 0, 1]
        ))
from numpy import zeros,sin,cos,array
#-------------------------------------------------------
# calculates the inverse of one or more transformations
#
#-------------------------------------------------------
def tinv(tab: array):
    tba = zeros((len(tab),1))
    for t in range(0,tab.shape[1], 3):
        tba[t:t+3,:] = tinv1(tab[t:t+3])
    return tba    

#-------------------------------------------------------
def tinv1(tab):
#
# calculates the inverse of one transformations
#-------------------------------------------------------
    s = sin(tab[2, 0])
    c = cos(tab[2, 0])
    x = tab[0,0]
    y = tab[1,0]
    a = tab[2,0]

    tba = array([
            [   -x*c - y*s    ],
            [    x*s - y*c    ],
            [   -a            ]
            ])

    return tba

def jac_tinv1(p):
    '''
        Calculate the jacovian d -p / d p
        p : Position at which tinv is evaluated
    '''
    x, y = p[0,0], p[1,0]
    s = sin(p[2,0])
    c = cos(p[2,0]) 

    return array([
        [ -c, -s, x*s-y*c ],
        [ s, -c, x*c+y*s ],
        [ 0, 0, -1 ]
    ])
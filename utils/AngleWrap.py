from numpy import pi

def AngleWrapList(a):
    id1 = a > pi
    a[id1] -= 2*pi
    id2 = a < -pi
    a[id2] += 2*pi
    return a

def AngleWrap(a):
    if a > pi:
        a -= 2*pi
    elif a < -pi:
        a += 2*pi
    return a
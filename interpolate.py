import numpy as np
from scipy import interpolate

def find_nearest(array,value):
    idx = np.searchsorted(array, value, side="left")
    if idx > 0 and (idx == len(array) or np.fabs(value - array[idx-1]) < np.fabs(value - array[idx])):
        return idx-1#array[idx-1]
    else:
        return idx#array[idx]


def biosig_interpolate(x1,y1,x2, Type):

    x1min = min(x1)
    x1max = max(x1)
    x2min = min(x2)
    x2max = max(x2)


    f = interpolate.interp1d(x1, y1)
    
    if x1min > x2min and x1max < x2max:
        #print "A"
        
        left = find_nearest(x2,min(x1))+1
        right = find_nearest(x2,max(x1))
    
        if Type == "A" or Type == "C":
            yinterp_left = np.zeros(left)
            yinterp_right = np.zeros(len(x2)-right)
        elif Type == "T":
            yinterp_left = np.ones(left)
            yinterp_right = np.ones(len(x2)-right)
        yinterp_middle = f(x2[left:right])
        yinterp = np.concatenate([yinterp_left,yinterp_middle, yinterp_right])

    elif x1min <= x2min and x1max < x2max:
        #print "B"
        right = find_nearest(x2,max(x1))
        
        if Type == "A" or Type == "C":
            yinterp_right = np.zeros(len(x2)-right)
        elif Type == "T":
            yinterp_right = np.ones(len(x2)-right)
        yinterp_middle = f(x2[:right])
        yinterp = np.concatenate([yinterp_middle, yinterp_right])
    
    elif x1min > x2min and x1max >= x2max:
        #print "C"
        left = find_nearest(x2,min(x1))+1
    
        if Type == "A" or Type == "C":
            yinterp_left = np.zeros(left)
        elif Type == "T":
            yinterp_left = np.ones(left)
        yinterp_middle = f(x2[left:])
        
        yinterp = np.concatenate([yinterp_left,yinterp_middle])
    
    else:
        #print "D"
        yinterp = f(x2)

    
    
    return yinterp

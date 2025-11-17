import matplotlib.pyplot as plt 
from matplotlib.patches import Circle, Wedge, Polygon
from matplotlib.collections import PatchCollection, LineCollection
import numpy as np

def getpoissondisc(n=100,sigma=1,distmin=0,trialsmax = 1000):
    # try:
    #     sample n points in [0,1]x[0,1]
    #     which centers have distance 2r+distmin
    # except:
    #     return those points that could have been
    #     sampled after a reasonable amount of time
    #     has passed
    r = sigma/n
    x = [] # store x,y values of points
    y = []
    trials = 0 # how often have we tried to generate a point 
    while len(x) < n:
        xi,yi = np.random.rand(),np.random.rand()
    
        for xj,yj in zip(x,y):
            dist = np.sqrt((xi-xj)**2+(yi-yj)**2)
            if dist < distmin+2*r:
                trials += 1
                break # this was one more trial, don't increase counter, don't add point
        else: # ohhhh  yeaaah for... else...
            x.append(xi)
            y.append(yi)
            trials = 0
        
        if trials > trialsmax:
            break
    x = np.asarray(x)
    y = np.asarray(y)
    r = np.ones(x.size)*r
    return x,y,r,x.size

def getrandompoints(n=100,sigma = 1):
    x = np.random.rand(n)
    y = np.random.rand(n)
    r = sigma/n*np.ones(n)
    return x,y,r,n

def getlatticepoints(n=100,sigma = 1,x0=0,x1=1,y0=0,y1=1):
    m = int(np.sqrt(n))
    dx = (x1-x0)/m/2
    x = np.linspace(x0+dx,x1-dx,m)
    y = np.linspace(y0,y1,m)
    xx, yy = np.meshgrid(x,y)
    x = np.reshape(xx,xx.size)
    y = np.reshape(yy,yy.size)
    r = sigma/n*np.ones(xx.size)
    return x,y,r,x.size

def getrotatedlatticepoints(n=100,alpha=0,sigma = 1):
    x,y,r,m = getlatticepoints(16*n,sigma,-2,2,-2,2)
    x,y = rotatepoints(x,y,alpha)
    condition = (0<x) & (x<1) & (0<y) & (y<1)
    xx = np.extract(condition,x)
    yy = np.extract(condition,y)
    rr = sigma/xx.size*np.ones(xx.size)
    nn = rr.size
    return xx,yy,rr,nn

def rotatepoints(x,y,alpha):
    sina,cosa = np.sin(alpha),np.cos(alpha)
    for i in range(len(x)):
        xx,yy  = x[i],y[i]
        x[i] = cosa*xx-sina*yy
        y[i] = sina*xx+cosa*yy
    return x,y

def plotpoints(x,y,radii):
    patches = []
    for x1, y1, r in zip(x, y, radii):
        circle = Circle((x1, y1), r)
        patches.append(circle)
    w = np.max(x)-np.min(x)
    h = np.max(y)-np.min(y)
    fig, ax = plt.subplots(figsize = (10*w,10*h))
    p = PatchCollection(patches)
    ax.add_collection(p)
    ax.axis('equal')
    plt.show()
    
def plotpointsandtrajectory(x,y,radii,X0,Y0,D):
    patches = []
    for x1, y1, r in zip(x, y, radii):
        circle = Circle((x1, y1), r)
        patches.append(circle)
    fig, ax = plt.subplots(1,1,figsize=(20,10))
    #ax = axs[0]
    p = PatchCollection(patches)
    ax.add_collection(p)
    ax.axis('equal')
    if type(X0)==float:
        ax.plot([X0,X0+D],[Y0,Y0])
    else:
        for x0,y0,d in zip(X0,Y0,D):
            ax.plot([x0,x0+d],[y0,y0],'r')
        #ax = axs[1]
        #plt.hist(D, 30, density=True);

    plt.show()
    
def pointbinning(x,y,r,nbins):
    bins = []
    maxr = np.max(r)
    edges = np.linspace(0,1,nbins+1)
    for i in range(nbins):
        idx = np.where((edges[i]-maxr<y) & (y<edges[i+1]+maxr))
        bins.append((x[idx],y[idx],r[idx]))
    return edges, bins


def getmanypoints(ns,sigmas,types,rotations):
    X,Y,R = [],[],[]
    i = 0
    for n,sigma,type,rot in zip(ns,sigmas,types,rotations):
        print(type)
        if type == "random":
            x,y,r,_ = getrandompoints(n,sigma) # no rotation needed since random
        elif type=="lattice":
            if rot == 0:
                x,y,r,_ = getlatticepoints(n,sigma)
            else:
                x,y,r,_ = getrotatedlatticepoints(n,rot,sigma)
        elif type=="poissondisc":
            x,y,r,_ = getpoissondisc(n,sigma,distmin = 0.2)
        else:
            print("ERROR, not yet implemented!")
            raise
        X = np.append(X,x+i)
        Y = np.append(Y,y)
        R = np.append(R,r)
        i+=1
    return X,Y,R, X.size
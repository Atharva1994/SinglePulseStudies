import numpy as np
import psrchive as psr

def getStokes(datain,dataout):
    dim=datain.shape
    for i in range(dim[0]):
        for j in range(dim[2]):
            dataout[i,0,j,:]=np.add(datain[i,0,j,:],datain[i,1,j,:])
            dataout[i,1,j,:]=np.subtract(datain[i,0,j,:],datain[i,1,j,:])
            dataout[i,2,j,:]=np.multiply(2,datain[i,2,j,:])
            dataout[i,3,j,:]=np.multiply(2,datain[i,3,j,:])

def getLinPol(datain,dataout):
    dim=datain.shape
    for i in range(dim[0]):
        for j in range(dim[2]):
            dataout[i,0,j,:]=datain[i,0,j,:]
            dataout[i,1,j,:]=np.sqrt(np.add(np.square(datain[i,1,j,:]),np.square(datain[i,2,j,:])))
            dataout[i,2,j,:]=np.divide(np.arctan(np.divide(datain[i,2,j,:],datain[i,1,j,:])),2)
            dataout[i,3,j,:]=datain[i,3,j,:]
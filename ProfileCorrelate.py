import psrchive as psr
import numpy as np
from SignalToNoise import *
from Stokes import *

def SubtractMean(datain,dataout,dim):

	for i in range(dim[0]):
		for j in range(dim[1]):
			for k in range(dim[2]):
				dataout[i,j,k,:]=np.subtract(datain[i,j,k,:],np.multiply(np.mean(datain[i,j,k,:]),np.ones(dim[3])))


def compute(dataFolder,datafile,initfreq,isStokes):
    arch=psr.Archive_load("/fred/oz005/users/akulkarn/J0437-4715/ProcessedDataAll/"+dataFolder+"/"+datafile)
    arch.fscrunch_to_nchan(16)
    arch.remove_baseline()
    #pol=0;
    

    BW=arch.get_bandwidth()
    CentFreq=arch.get_centre_frequency()
    nchan=arch.get_nchan()

    data=arch.get_data()

    dim=data.shape
    freq_f=np.linspace((CentFreq-(BW/2)+(BW/(2*dim[2]))),(CentFreq+(BW/2)-(BW/(2*dim[2]))),num=dim[2])

    R1=np.ndarray([dim[0],dim[1],dim[2],dim[2]]); 
    R1_mean=np.ndarray([dim[2],dim[1]]); 
    R1_std=np.ndarray([dim[2],dim[1]])
    data_mean=np.ndarray(dim); data_stokes=np.ndarray(dim);  
    ArchSNR=np.ndarray([dim[0],dim[2]]); 

    R1_mean_plot_f=np.ndarray([dim[2],dim[1]]) ; 
    R1_std_plot_f=np.ndarray([dim[2],dim[1]]); 
    R1_stder_plot_f=np.ndarray([dim[2],dim[1]]);
    
    if (isStokes==True):
        getStokes(data,data_stokes)
    else:
        data_stokes=data
    
    SubtractMean(data_stokes,data_mean,dim) 
    
    ArchiveSNR(arch,dim,ArchSNR)
    
    for i in range(dim[0]):
        for j in range(dim[1]):
            R1[i,j]=np.corrcoef(data_mean[i,j,:,:])

        
    #rows=int(dim[2]/4); cols=int(4); #initfreq=6;

    ############################# For computing mean and standard deviation of varaition in correlation coefficient at all frequencies  ##############################

    #for i in range(rows):
    #    for j in range(cols):
    #        for k in range(dim[1]):
    #            R1_mean[cols*i+j,k]=np.mean(R1[:,k,initfreq,cols*i+j]); 
    #            R1_std[cols*i+j,k]=np.std(R1[:,k,initfreq,cols*i+j])

    for i in range(dim[2]):
        for k in range(dim[1]):
            R1_mean[i,k]=np.mean(R1[:,k,initfreq,i]); 
            R1_std[i,k]=np.std(R1[:,k,initfreq,i])

            


    ################################# For plotting the mean and standard Deviation of the measured correlation coefficient as a function of frequency..######################

    
    for i in range(dim[2]):
        if i==initfreq:
            R1_mean_plot_f[i]=np.nan
            R1_std_plot_f[i]=np.nan
            R1_stder_plot_f[i]=np.nan
        else:
            R1_mean_plot_f[i]=R1_mean[i]
            R1_std_plot_f[i]=R1_std[i]
            R1_stder_plot_f[i]=np.multiply(1.96,np.divide(R1_std[i],np.sqrt(dim[0])))

    #R1_stder_plot=np.multiply(1.96,np.divide(R1_std_plot,np.sqrt(dim[0])))

    #Axs1.errorbar(x=np.around(freq,decimals=2),y=R1_mean_plot_f[count,:],yerr=R1_stder_plot_f[count,:],marker='x',label=datafile)
    return R1_mean_plot_f, R1_std_plot_f, R1_stder_plot_f, freq_f, ArchSNR
    
    #count=count+1

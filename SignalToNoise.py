import psrchive as psr
import numpy as np

def ArchiveSNR(arch,dim,ArchSNR):
	for i in range(dim[0]):
		Intg=arch.get_Integration(i)
		for j in range(dim[2]):
			Prof=Intg.get_Profile(0,j)
			ArchSNR[i,j]=Prof.snr()
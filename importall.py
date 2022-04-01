#import matplotlib.pyplot as plt
import numpy as np
import psrchive as psr
from SignalToNoise import *
from Stokes import *
from ProfileCorrelate import *

compute_num=np.frompyfunc(compute,4,5)
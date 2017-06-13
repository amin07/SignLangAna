import numpy as np
import scipy as sp
import sys
from scipy import stats
import plt from matplotlib.pyplot 
import get_features as gfe
import get_filter as gfi
from _signal import signal
from tensorflow.python.kernel_tests.parsing_ops_test import feature
 
# set the butter filter and cut frequency
filter_order = 3
 
# filename = sys.argv[1]
# f = open(filename)
# filelist = f.readlines()
# get the bandpower and difftime
# bandpower = []
# difftime = []
# for i in range(1,len(filelist)):
#     bandpower.append(float(filelist[i].split(', ')[2].replace('\r', '').replace('\n', '')))
#     difftime.append(float(filelist[i].split(', ')[1]))
#  

# reading samples from data file
'''
filename = 'long_dist_file.csv'
f = open(filename)
file_rows = f.readlines()
for _row in file_rows:
    print (_row)
'''
signal_data = np.genfromtxt('long_dist_file.csv', delimiter = ',')[:,1:]

feature_mat = []
for i in range(15): 
    bandpower = signal_data[i]
    # calculate the samples rate and sample spacing
    samples = len(bandpower)
    #total_time = float(difftime[-1])
    # get the samples rate, taking each instance as 8 second
    sample_rate = samples/8
    # calculate the sample spacing
    ss = 1./sample_rate
     
    # get Nyquist frequency
    nyq = 0.5 * sample_rate
    # transfer bandpower to nparray
    bp = np.asarray(bandpower)
     
    # get the filtered data 
    bandpassed_data = gfi.band_pass(bp, 0.1, 20, nyq, filter_order)
    active_band_data = gfi.band_pass(bp, 0.3, 3.5, nyq, filter_order)
    modvig_band_data = gfi.band_pass(bp, 0.71, 10, nyq, filter_order)
    lowpassed_data = gfi.low_pass(bp, 1, nyq, filter_order)
    low_band_data = gfi.low_pass(bp, 0.7, nyq, filter_order)
     
    # calculate the features
    DCMean = gfe.getMean(lowpassed_data)
    DCArea = gfe.getArea(lowpassed_data)
     
    ACAbsMean = gfe.getAbsMean(bandpassed_data)
    ACEntropy = gfe.getEntropy(bandpassed_data)
    ACSkew = gfe.getSkew(bandpassed_data)
    ACKur = gfe.getKur(bandpassed_data)
    ACQs = gfe.getQuartiles(bandpassed_data)
     
    ACVar = gfe.getVar(bandpassed_data)
    ACAbsCV = gfe.getAbsCV(bandpassed_data)
    ACIQR = gfe.getIQR(ACQs[2], ACQs[0])
    ACRange = gfe.getRange(bandpassed_data)
     
    ACFFTCoeff = gfe.getFFTCoeff(bandpassed_data)
    ACFFTPeaks = gfe.getFFTPeaks(bandpassed_data)
     
    ACEnergy = gfe.getEnergy(bandpassed_data)
    ACBandEnergy = gfe.getEnergy(active_band_data)
    ACLowEnergy = gfe.getEnergy(low_band_data)
    ACModVigEnergy = gfe.getEnergy(modvig_band_data)
     
    ACPitch = gfe.getPitch(bandpassed_data)
    ACDomFreqRatio = gfe.getDomFreqRatio(bandpassed_data)
    ACMCR = gfe.getMCR(bandpassed_data)
     
    features = []
    features.append(DCMean)
    features.append(DCArea)
    features.append(ACAbsMean)
    features.append(ACEntropy)
    features.append(ACSkew)
    features.append(ACKur)
    features.extend(ACQs)   #extend because returning array/list
    features.append(ACVar)
    features.append(ACAbsCV)
    features.append(ACIQR)
    features.append(ACRange)
    features.append(ACEnergy)
    features.append(ACBandEnergy)
    features.append(ACLowEnergy)
    features.append(ACModVigEnergy)
    features.append(ACPitch)
    features.append(ACDomFreqRatio)
    features.append(ACMCR)
    features.extend(ACFFTCoeff)
    features.extend(ACFFTPeaks)
    feature_mat.append(features)

#for i in range(15):
#    print (feature_mat[i])
ar = np.array(feature_mat)
#print (ar)



#distance calculation
dist_mat = np.zeros((15,15))
for i in range(15):
    for j in range(15):
        dist_mat[i,j] =  (sp.spatial.distance.euclidean(ar[i], ar[j]))

print (dist_mat)

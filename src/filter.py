from scipy import signal
import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
import sys
import csv
# set the butter filter and cut frequency
filter_order = 3
cutoff_low = 5
cutoff_high = 60

#filename = sys.argv[1]
file_dir = 'C:/Users/admin_user/data_sets/experiment/0608/0608/long_distance/'
file_list = ['school_RSSI','mother_RSSI','deny_RSSI']

out_file = open('long_dist_file.csv','w',newline='')
csvwriter = csv.writer(out_file)

for f_list in file_list:
    filename = file_dir + f_list+'.csv'
    f = open(filename)
    filelist = f.readlines()
    # get the bandpower and difftime
    bandpower = []
    difftime = []
    for i in range(1,len(filelist)):
        bandpower.append(float(filelist[i].split(', ')[2].replace('\r', '').replace('\n', '')))
        difftime.append(float(filelist[i].split(', ')[1]))
    
    samples = len(bandpower)
    total_time = float(difftime[-1])
    print ('total time', total_time,'total samples', samples)
    
    # get the samples rate
    sample_rate = samples/total_time
    # calculate the sample spacing
    ss = 1./sample_rate
    
    
    
    # get Nyquist frequency and compute the low and high for butter
    nyq = 0.5 * sample_rate
    low = cutoff_low / nyq
    high = cutoff_high / nyq
    if (high >= 1):
        high = float(0.99)
    if (low >= 1):
        low = float(0.99)
    
    
    #for filter_order in range(1,7):
    b, a = signal.butter(filter_order, [low, high], btype='band')
    # computer the time
    t = np.linspace(0, total_time, samples)
    # convert list to ndarray
    bp = np.asarray(bandpower)
    # plot the figure
    filtered_data = signal.filtfilt(b, a, bp)
    afd = abs(filtered_data)
    smoothed_data = sp.ndimage.filters.median_filter(afd,150)
    print ('smoothed data len', len(smoothed_data))

    roi_data_start = 3
    roi_data_range = 8
    
    # dividing continuous 5 samples into 5 different samples
    # smoothed_data = smoothed_data.tolist()
    row_list = []
    for i in range(5):
        #print (smoothed_data[roi_data_start:(roi_data_start+roi_data_range)])
        instance_sample = [f_list+'_'+str(i)]
        instance_sample.extend([smoothed_data[i] for i in range(len(t)) if t[i] >=roi_data_start and t[i]<(roi_data_start+roi_data_range)])
        
        print ('inst sample len', len(instance_sample))
        row_list.append(instance_sample)
        roi_data_start += 10
        
    csvwriter.writerows(row_list)
    #plt.plot(t, afd )
    #plt.ylabel('band power')
    #plt.xlabel('time')
    #plt.show()
    
    #plt.plot(t, signal.savgol_filter(afd,9,3))
#     plt.plot(t, sp.ndimage.filters.median_filter(afd,150))
#     plt.ylabel('smooth band power')
#     plt.xlabel('time')
#     plt.savefig(filename+"_filtered2.png")
#     plt.close()


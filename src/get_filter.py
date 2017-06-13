from scipy import signal
 
# return the filtered data through a bandpass filter
def band_pass(bp, cutoff_low, cutoff_high, nyq, filter_order = 3):
    low = cutoff_low / nyq
    high = cutoff_high / nyq
    b, a = signal.butter(filter_order, [low, high], btype='band')
    filtered_data = abs(signal.filtfilt(b, a, bp))
    return filtered_data
 
# return the filtered data through a low pass filter
def low_pass(bp, low_pass, nyq, filter_order = 3):
    low = low_pass / nyq
    b, a = signal.butter(filter_order, low, btype='low')
    filtered_data = abs(signal.filtfilt(b, a, bp))
    return filtered_data
# return the filtered data through a high pass filter
def high_pass(bp, high_pass, nyq, filter_order = 3):
    high = high_pass / nyq
    b, a = signal.butter(filter_order, high, btype='high')
    filtered_data = abs(signal.filtfilt(b, a, bp))
    return filtered_data
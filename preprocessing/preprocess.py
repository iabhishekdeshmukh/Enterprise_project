
from scipy import stats
import pandas as pd
import pickle
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import math
import time
from scipy import stats
from scipy.signal import find_peaks


#returns start and end points of each bore cutting based on pos_z axis value with fixed threshold
def cutting_samples(pos_z): 
    start=[]
    end=[]
    mode1 = stats.mode(pos_z)[0][0]  #works with pos_z = dataframe
    mode1 = math.trunc(mode1)  #Only int part
    for i in range(len(pos_z)):
        whole_part = math.trunc(pos_z[i])
        if whole_part==mode1:
            whole_next_part = math.trunc(pos_z[i+1])
            whole_prev_part = math.trunc(pos_z[i-1])
            if whole_prev_part > whole_part :
                start.append(i)
            elif whole_next_part > whole_part:
                end.append(i)
    
    return start, end  #return arrays of start and end sample points


def extract_pos_z(df1):
    pos_z = df1['Lageistwert_Z'].to_numpy()
    pos_z = pos_z.reshape(len(df1),)
    pos_z = pos_z.astype(np.float)
    
    return pos_z


def extract_cutting_intervals_level_1(pos_z):
    cutting_pos_z = []
    cutting_sample = []
    
#    plt.figure(figsize=(16,16))
#     x,y = sns.kdeplot(pos_z).get_lines()[0].get_data()
#     plt.close()
    max1 = stats.mode(pos_z)[0][0]
    
    lower_threshold = max1 - 0.2
    higher_threshold = max1 + 0.2
    
    for i in range(len(pos_z)):
        #whole_part = math.trunc(pos_z[i])
        if pos_z[i]>= lower_threshold and pos_z[i]<= higher_threshold:
            cutting_pos_z.append(pos_z[i])
            cutting_sample.append(i)
                
    return cutting_pos_z, cutting_sample, max1            
        

def find_cutting_height(y_values):# calculate mode and accept only a little fractal of the standarddeviation around it as cutting height of the z-axis
    mode_value = stats.mode(y_values)[0]
    std_value = np.std(y_values)
    cutting_height = mode_value + std_value/100
    return(cutting_height)

def find_cutting_time(y_values): # Defines a function that finds starting point and end point of each cutting process
    start_cutting = []
    end_cutting = []
    ch = find_cutting_height(y_values = y_werte)
    for i in range(len(y_values)):
        if i < 1:
            continue
        if y_values[i] < ch and y_values[i-1] >= ch:#96.825#96.605
            start_cutting.append(i)
    for i in range(len(y_values)):
        if i < 1:
            continue
        if y_values[i] >= ch and y_values[i-1] < ch:
            end_cutting.append(i-1)
    return(start_cutting, end_cutting)

def find_peaks(y_values): # uses the find_cutting_time function to create a list of tupels, consisting of the actual cutting processes (start-index, end-index)
    peaks = []
    start, end = find_cutting_time(y_values = y_werte)
    for j in range(len(start)):
        peaks.append((start[j], end[j]))
    return(peaks)  

def find_peak_timesections(y_values): # converts the tupels into a list of indices that refer to the cutting process
    timesections_to_filter_out = []
    peaks = find_peaks(y_values)
    for k in range(len(peaks)):
        if k == 0:
            num = peaks[k][0]
            timesections_to_filter_out.append((np.linspace(0, peaks[k][0], num+1)).tolist())
        else:
            num = peaks[k][0]-peaks[k-1][1]
            timesections_to_filter_out.append((np.linspace(peaks[k-1][1] ,peaks[k][0], num+1)).tolist())
    return(timesections_to_filter_out)

def build_list_of_indices_to_drop(y_values): # takes the output of find_peak_timesections to convert it into a single list of indices that afterwards can be dropped by using "df.drop(indices)"
    indices_to_drop = []
    timesections = find_peak_timesections(y_values= y_werte)
    for timesection in timesections:
        for index in timesection:
            indices_to_drop.append(int(index))
    return(indices_to_drop)


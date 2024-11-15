import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import time
import os
import shutil
from os import listdir
from os.path import isfile, join
from scipy.signal import find_peaks
from itertools import chain


plt.style.use('figuras_lucio.mplstyle')


def get_peaks(data,time,height = None, prominence = None,threshold = None):
    
    peak_index = find_peaks(-data,height = height, prominence = prominence,threshold = threshold)
    peaks_t = np.array([time[i] for i in peak_index[0]])
    peaks_signal = np.array([data[i] for i in peak_index[0]])

    return peaks_signal, peaks_t

def histograma(path,iteracion,title = False,prominence = None, height = None,threshold = None,bin_start = None,bin_end = None,bin_num = 50):
    peaks_voltage = []
    folder = f'Iteración {iteracion}'
    path = join(path,folder)
    onlyfiles = [file for file in listdir(path) if isfile(join(path, file))]
    for file in onlyfiles:
        df = pd.read_csv(join(path, file))
        t = df['Datos'].values
        d = df["Tiempo"].values
        peaks, peaks_t = get_peaks(d,t,prominence = 0.01, height = None,threshold = None)

        peaks_voltage.append(peaks)

    # flattened_peaks = np.array([value for value in peaks_voltage[j] for j in range(len(peaks_voltage))])
    flattened_peaks = flatten_chain(peaks_voltage)
    flattened_peaks_mv = np.array(flattened_peaks) * 100
    # print(len(peaks_voltage[0]))
    # print(len(flattened_peaks))    
    #  
    d_mean = np.mean(d*100)
    d_std = np.std(d*100)

    #Histograma --------------------------------------------------------------------------------------------

    fig, ax = plt.subplots()
    bin_start = -6.5
    bin_end = 0
    bin_num = 50
    bins = np.linspace(bin_start,bin_end,endpoint = True,num = bin_num)
    # print(bins[1]-bins[0])
    # print(bins);
    ax.hist(x = flattened_peaks_mv, bins = bins);
    ax.set_xlim(bins[0],0)

    xlabels = np.arange(bins[0],0.5,0.5,)
    ax.set_xticks(xlabels)
    ax.set_xticklabels([f'{number:.1f}' for number in xlabels]);

    ax.set_ylabel(f'Eventos')
    ax.set_xlabel(f'Voltaje [mV]')
    ax.axvline(x = d_mean - d_std, ymin = 0, ymax = 1,color = 'tomato',linestyle = '--')
    ax.annotate(f' Prominence: {prominence}\n Bin size: {abs(bin_start-bin_end)/bin_num}\n Threshold: {threshold}\n Height: {height}',(0.8,0.75),xycoords='axes fraction',fontsize = 13)
    if title:
        ax.set_title(f'{path}')

    return fig
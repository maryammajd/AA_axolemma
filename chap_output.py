#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  2 19:13:42 2023

this script reads the data from the jason file made by gmx_analyze_Ka_jason_maker.py file. the json file exist for both 
ten and pxx.
@author: maryamma
"""

import matplotlib.pyplot as pyplot
import numpy as np
import scipy.stats as stats
import json
import statsmodels.api as sm
# import pdb; pdb.set_trace()


def json_read(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)
    return data

def mean_value(data, mean_step):
    mean_data = []
    for i in range(1, int((len(data)-1)/mean_step)+1):
        mean_data.append(np.mean(data[(i-1)*mean_step:i*mean_step]))
    return mean_data

def xvg_read(dir, var):
    time, data = [], []
    temp_data = np.genfromtxt(
        (r for r in open(str(dir) + str(var) + '.xvg') if not r[0] in ('@', '#', '&')))
    for i in range(len(temp_data.T[0])):
        if temp_data.T[0][i] % 1000 ==0: 
            time.append(temp_data.T[0][i])
            data.append(temp_data.T[1][i])
    return time, data

source_dir = '/run/media/maryamma/One Touch/project_md/project_2/analysis241205/'

parameters = ['numPathway','numSample', 'poreRadius' , 'volume', 'minSolventDensity', 'minRadius' ]
key_param = 'pathwayScalarTimeSeries'

parameters =  ['densityMean', 'radiusMean']
key_sum = 'pathwayProfile'

# dirs=["eq", "deform/10-4", "deform/10-4/eq/0.20", "deform/10-4/eq/0.35m", "deform/10-4/eq/0.45m" ]
dirs= ["eq", "deform/10-4"]
      #, "deform/10-4/eq/0.20", "deform/10-4/eq/0.35m", "deform/10-4/eq/0.45m" ]

cmap = pyplot.get_cmap('viridis')


timepoint = [-1000, -1000, 42500, 74400, 95900] # time where each deformation happens
begining_times = np.arange(0,50000,1000)

colors = cmap(np.linspace(0, 1, len(begining_times)))

mean_step = 5

for parameter in parameters: # parameters:
    max_den = 0
    for begining_time in begining_times:

        key = key_sum # key_param
        for num, dir in enumerate(dirs):
            file = source_dir + dir + f'/chap-{begining_time}-{begining_time+1000}.json'
            file_chap = json_read(file)
            time = file_chap[key]['s']
            param = file_chap[key][parameter] # ['mean']
            # time = np.arange(0, len(param))
            # t2, box = xvg_read( source_dir + dir, '/boxx')
            for i in range(len(param)):
                if param[i] < 0:
                    print(i)
                    param[i] =0
                elif param[i] > 1000000000000:
                    param[i] = 0
            mean_time_eq = mean_value(np.array(time), mean_step)
            mean_param_eq = mean_value(np.array(param), mean_step)

            if num != -1: # or num == 0:
                pyplot.plot(time,param, color= colors[int(begining_time/1000)], label = str(begining_time))

            # pyplot.axhline(y= np.mean(param), label = dir, color= colors[num])
            # pyplot.scatter(x= timepoint[num], y = np.mean(param), color = colors[num])

        pyplot.title(parameter + str(begining_time))
        # pyplot.xlim(0,150000)
        pyplot.legend(loc='best')
        pyplot.savefig( source_dir + parameter)
        pyplot.show()
            # print(file_chap.keys())


"""
Created on Thu Aug 29 15:13 2024
reading xvg files for some params and compare with their state in equilibrium
@author: maryamma
"""
import numpy as np
from math import sqrt
import matplotlib.pyplot as pyplot
import matplotlib as plt
import scipy.stats as stats
import statsmodels.api as sm
from matplotlib.ticker import (MultipleLocator)
import os
# import pdb; pdb.set_trace()
cmap = pyplot.get_cmap('viridis')

def xvg_read(directory, var):
    temp_data = np.genfromtxt(
        (r for r in open(str(directory) + str(var) + '.xvg') if not r[0] in ('@', '#', '&')))
    time = temp_data.T[0]
    data = temp_data.T[1]
    return time, data

def mean_value(data, mean_step):
    mean_data = []
    for i in range(1, int((len(data)-1)/mean_step)+1):
        mean_data.append(np.mean(data[(i-1)*mean_step:i*mean_step]))
    return mean_data
mean_step = 20
source_dir = "/run/media/maryamma/One Touch/project_md/project_2/analysis241205/"

simulation_dir = ['eq/', # "deform/10-4/eq/0.20/", 
        # "deform/10-4/", 
        "deform/10-4/eq/0.20/", 
        "deform/10-4/eq/0.35m/", 
        "deform/10-4/eq/0.45m/", "deform/press75/"
        # , "deform/z-def/" ,"deform/z-press/press75/"
        ]
colors = cmap(np.linspace(0, 1, len(simulation_dir)))
# 'gyrate-taf':'radius', 
params = {'gyrate-all':'number', 'gyrate-protmemb':'number',
          'hbnum-all':'number', 'hbnum-protmemb':'number', 
          'hbnum-vsd1':'number', 'hbnum-vsd2':'number', 'hbnum-vsd3':'number', 'hbnum-vsd4':'number', 'sasa-protmemb':"Area", 
          'rmsf-protmemb': 'nm'
          # 'thickness': 'mm', 'interdigitation': '%'
          }

# for simulations in simulation_dir:
for param in params.keys():
    print(param)
    for sim_num, simulations in enumerate(simulation_dir):
        directory_eq = os.path.join(source_dir, simulation_dir[0], 'analyse/')
        time_eq, hbnum_eq = xvg_read(directory_eq, param)

        mean_hbnum_eq = mean_value(np.array(hbnum_eq), mean_step)

        directory = os.path.join(source_dir, simulations, 'analyse/')
        time, hbnum = xvg_read(directory, param)

        mean_hbnum = mean_value(np.array(hbnum), mean_step)
        mean_time_hbnum = mean_value(np.array(time), mean_step)
        print(simulations)
        # fig = pyplot.figure(figsize=(1.2*5, 5), dpi=300)

        pyplot.plot(time, np.array(hbnum), color=colors[sim_num],
                        label=simulations, zorder = 1)
        pyplot.plot(mean_time_hbnum, mean_hbnum, color=colors[sim_num], linestyle='dashed'
                        # label=simulations + 'mean'
                        )
        # pyplot.plot(time_eq, np.array(hbnum_eq), color='pink',
        #                label='eq', zorder = 0)
        # # pyplot.axhline(y=np.mean(hbnum), color='silver', label = 'deformation-mean')#, linestyle='-', zorder=2)
        # pyplot.axhline(y=np.mean(hbnum_eq), color='red', label = 'eq-mean')#, linestyle='-', zorder=2)
    pyplot.legend(loc='right')
    pyplot.title(f'{params[param]} of {param} in eq and under deformation')
    pyplot.xlabel('time')
            # pyplot.ylabel(f'{params[param]}')
        #pyplot.savefig(f'{directory}/{param}-comparison.png')
    pyplot.savefig(f'{source_dir}/{param}.png')
        # pyplot.show()
    pyplot.close()

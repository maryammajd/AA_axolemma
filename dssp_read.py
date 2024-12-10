"""
This code is used to calculates how many times the 2ndary structures of a residue of a protein is changed in a simulation when compared with average protein structure in equilibrium.

For this purpose, first run gmx dssp for each simulation to get a dat file including the 2ndary structure of the desired part of protein in each timeframe. Remember to always use the same structure (.gro file) for -s option of all the simulations you are comparing with each other.

Then run this code to find how the structure differs with the average one. The ref model is defined as the first element in simulation_dir array in the code. 
"""
import numpy as np
from math import sqrt
import matplotlib.pyplot as pyplot
import scipy.stats as stats
import statsmodels.api as sm
from matplotlib.ticker import (MultipleLocator)
import os
import csv
import pdb; pdb.set_trace()

def dat_read(directory, var):
    with open(str(directory) + str(var) + '.dat', 'r') as file:
        lines = file.readlines()
    temp_data = [[char for char in line.strip()] for line in lines]
    return np.array(temp_data)

def changed_frames(data, ref):
    changes = {}
    for resid in range(data.shape[1]):
        changes[resid] = []
        for time_frame in range(data.shape[0]):
            if not (ref[0][resid] == data[time_frame][resid]):
                changes[resid].append(time_frame)
    return changes

def change_repetitions(changes, lower_bound, upper_bound):
    changed_resids = []
    for resid, timeframe in changes.items():
        if len(timeframe) > lower_bound and len(timeframe) < upper_bound:
            changed_resids.append(resid)
    return changed_resids
    
source_dir = "/run/media/maryamma/One Touch/project_md/"

simulation_dir = ['project_2/gromacs/2fs/',  'project_2/gromacs/deform/10-4/', 'project_2/gromacs/deform/10-4/eq/0.45m/']
between_0_10, between_10_100, between_100_inf = {}, {}, {}
for simulation_num in range(len(simulation_dir)):
    directory = os.path.join(source_dir, simulation_dir[simulation_num])

    data = dat_read(directory, 'dssp')
    if simulation_num == 0:
        ref = dat_read(directory, 'dssp-ref')

    changes = changed_frames(data, ref)

    between_0_10[simulation_num] = change_repetitions(changes,0,10)
    between_10_100[simulation_num] = change_repetitions(changes,10,100)
    between_100_inf[simulation_num] = change_repetitions(changes,100,float('inf'))

    print(f'for {simulation_dir[simulation_num]}, {len(between_0_10[simulation_num])} res. changed less than 10 times,  {len(between_10_100[simulation_num])} residues are changed between 10 to 100 times and  {len(between_100_inf[simulation_num])} residues are changed more than 10 times')
print('finish')

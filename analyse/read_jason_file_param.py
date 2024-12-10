#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  2 19:13:42 2023

this script reads the data from the jason file made by gmx_analyze_Ka_jason_maker.py file. the jason file exist for both 
ten and pxx.
@author: maryamma
"""

import matplotlib.pyplot as pyplot
import numpy as np
import scipy.stats as stats
import json
import statsmodels.api as sm
import pdb; pdb.set_trace()
all_variables = [('sasa-protmemb', 'sasa', '[nm/S2/N]', 'area-time'),
                 ('gyrate-membprot', 'gyration radius', '[nm]', 'gyrate-time'),
                 ('hbnum-membprot', 'hydrogen bonds', '[#]', 'hb-time')]


for var, var_name, unit, calcuated_var in all_variables:
    print(f'Data for {var}')
    json_file = f'/run/media/maryamma/One Touch/project_md/project_2/{var}_data_from_const_area.json'


    color = ['#377eb8', '#ff7f00', '#4daf4a', 'crimson', 'yellow']
    systems = ["Axolemma", "one-protein-axolemma", "Node-of-Ranvier", "Myelin"]
    fig = pyplot.figure(figsize=(1.2*5, 5), dpi=400)

    # Read JSON data from the file
    with open(json_file, 'r') as file:
        data = json.load(file)
    # print(data.keys())
    # Now 'data' contains the JSON data as a Python dictionary
    for model_num, first_level_keys in enumerate(data.keys()):
        time, tension_ave, tension_err = [], [], []
        # print(second_level_keys)
        # print(first_level_keys, second_level_keys,
        #       (data[first_level_keys]['average']))
        # if first_level_keys != 'eq':
        ave_local = data[first_level_keys]['average']
        time_local = np.array(data[first_level_keys]['begin_time'], dtype=float)
        ave_local_float = np.array(ave_local, dtype=float)
        tension_ave.extend(ave_local_float)
        time.extend(time_local)
        err_local = data[first_level_keys]['st_err']
        err_local_float = np.array(err_local, dtype=float)
        tension_err.extend(err_local_float)

        # print(f"y = {m}x + {b}")

        pyplot.errorbar(time, tension_ave,  yerr=tension_err,
                        linestyle="none", marker='o', ms=3, elinewidth=2, color=color[model_num], label = first_level_keys)  # mfc='w',
        pyplot.xlabel('areal strain', size=12)
        pyplot.ylabel(var_name + unit, size=12)

    # pyplot.axhline(y=0, color='salmon', zorder=600)
    pyplot.title(var_name)
    pyplot.legend(loc='best')
    pyplot.savefig(f'{var_name}.png')
    pyplot.show()

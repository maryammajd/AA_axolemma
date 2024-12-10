#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 30 08:51:50 2024

@author: maryamma
"""

import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as ticker


relative_neighboring, ratio_l_x, enrichment_factor = {}, {}, {}

# =============================================================================
# # Node:
# ratio_bulk = {"pc-up": 38.61, "pe-up": 18.87, "sm-up": 6.66, "gl-up": 36.26, "pc-down": 26.87, "pe-down": 46.36,
#               "sm-down": 3.08, "pi-down": 13.42, "ps-down": 9.89}
#
#
# # axl-prot:
# ratio_bulk = {"pc-up": 0.37, "pe-up": 0.19, "sm-up": 0.06,
#               "gl-up": 0.38, "pc-down": 0.26, "pe-down": 0.48, "sm-down": 0.02, "pi-down": 0.14, "ps-down": 0.10}
#
# =============================================================================

# directories = ["/run/media/maryamma/One Touch/project_md/CG-axl-prot/small/node/eq/no-pos-res/neighbor/neighbor-all/",
#                "/run/media/maryamma/One Touch/project_md/CG-axl-prot/large/equilibrium/30us/neighbor/"]
# systems = ['node', 'large']

directories = ["/run/media/maryamma/One Touch/project_md/project_2/gromacs/step7/no-posres/neighboring-com/",
               "/run/media/maryamma/One Touch/project_md/project_2/gromacs/2fs/neighboring-com-200/"]
systems = ["1fs", "2fs"]
absolute_neighboring, relative_neighboring = {}, {}
colnames = ['time', 'number']
comment_chars = ['@', '#']
for system_num, (dir, system_chosen) in enumerate(zip(directories, systems)):
    # print(system_chosen)
    # print(dir, system_chosen, '***')

    first_folder_list = [d for d in sorted(
        os.listdir(dir)) if os.path.isdir(os.path.join(dir, d))]
    # first_folder_list = ['pc-down', 'pe-down',
    #                      'pe-up', 'pi-down', 'ps-down', 'sm-down', 'sm-up']
    # print(first_folder_list)
    absolute_neighboring[system_chosen], relative_neighboring[system_chosen] = {
    }, {}
    ratio_l_x[system_chosen] = {}
    for first_folder in first_folder_list:
        # =============================================================================
        #         grid_size_rel[first_folder] = {}
        #         grid_size_rel[first_folder]['max'] = 0
        #         grid_size_rel[first_folder]['min'] = 1
        # =============================================================================
        if not first_folder.startswith('ch'):
            # print(first_folder)
            second_folder_list = [d for d in sorted(os.listdir(dir + '/' + first_folder)) if os.path.isdir(
                os.path.join(dir + '/' + first_folder, d)) and not d.startswith('.')]
            # second_folder_list = ['pc-pc-down']
            # print(second_folder_list)
            for second_folder in second_folder_list:
                # print(second_folder)
                if second_folder.startswith('al-'):
                    new_dir = dir + first_folder + '/' + second_folder
                    filename_list = sorted(os.listdir(new_dir))
                    data_frame_all = pd.DataFrame()
                    os.chdir(new_dir)
                    # print(new_dir)
                    df = pd.read_csv(
                        new_dir + '/' + second_folder + '.xvg', delimiter=' ')
                    df.columns = ['time', 'number', 'number2']
                    time_ref = df['time'].astype(
                        float).to_numpy()/1000000 + system_num/10
                    neighboring_value_ref = df['number'].astype(
                        float).to_numpy()
            for second_folder in second_folder_list:
                if not second_folder.startswith('CH') and not second_folder.startswith('al'):
                    # print(second_folder)
                    new_dir = dir + first_folder + '/' + second_folder
                    filename_list = sorted(os.listdir(new_dir))
                    data_frame_all = pd.DataFrame()
                    os.chdir(new_dir)
                    # print(new_dir + '/' + second_folder + '.xvg')
                    df = pd.read_csv(
                        new_dir + '/' + second_folder + '.xvg', delimiter=' ')
                    df.columns = ['time', 'number', 'number2']
                    # print(df)
                    time = df['time'].astype(float).to_numpy()/1000000
                    neighboring_value = df['number'].astype(float).to_numpy()
                    relative = []
                    for rel_num in range(0, len(neighboring_value)):
                        relative.append(
                            np.round(neighboring_value[rel_num]/neighboring_value_ref[rel_num], 4))
                    absolute_neighboring[system_chosen][second_folder] = neighboring_value
                    relative_neighboring[system_chosen][second_folder] = relative
# =============================================================================
#                     grid_size_rel[first_folder]['max'] = max(
#                         grid_size_rel[first_folder]['max'], max(relative))
#                     grid_size_rel[first_folder]['min'] = min(
#                         grid_size_rel[first_folder]['min'], min(relative))
# =============================================================================
    for leaflet in ['upper', 'lower']:
        grid_size_rel = {}
        keys = list(key for key in relative_neighboring[system_chosen].keys(
        ) if key.endswith(leaflet))
        values = list(value for key, value in relative_neighboring[system_chosen].items(
        ) if key.endswith(leaflet))
        # print(keys)
        # Calculate the number of rows and columns for a square grid
        num_plots = len(keys)
# =============================================================================
#         num_cols = 5
#         num_rows = int(num_plots / num_cols)
# =============================================================================
        num_rows = int(np.sqrt(num_plots))
        num_cols = int(np.ceil(num_plots / num_rows))
        for second_lipid_num in range(0, num_cols):
            grid_size_rel[second_lipid_num] = {}
            grid_size_rel[second_lipid_num]['max'] = 0
            grid_size_rel[second_lipid_num]['min'] = 1
        # Set up subplots in a square grid
        fig, axes = plt.subplots(
            nrows=num_rows, ncols=num_cols, figsize=(1.2*3*num_cols, 3*num_rows))
        for idx, (key, value) in enumerate(zip(keys, values)):

            ratio_l_x[system_chosen][key] = round(np.mean(value), 4)
            row = idx // num_cols
            col = idx % num_cols
            grid_size_rel[col]['max'] = max(
                grid_size_rel[col]['max'], max(value))
            grid_size_rel[col]['min'] = min(
                grid_size_rel[col]['min'], min(value))
            axes[col, row].errorbar(time, value, color='black')
            axes[col, row].set_title(key)
            axes[col, row].axhline(ratio_l_x['1fs'][key], color='red')
            if col != num_cols-1:  # Hide x-ticks and labels for all but the first row
                axes[col, row].set_xticklabels([])
                axes[col, row].set_xlabel('')
            if row != 0:  # Hide y-ticks and labels for all but the first column
                axes[col, row].set_yticklabels([])
                axes[col, row].set_ylabel('')
        for idx, (key, value) in enumerate(zip(keys, values)):
            row = idx // num_cols
            col = idx % num_cols
            axes[col, row].set_ylim(
                grid_size_rel[col]['min'], grid_size_rel[col]['max'])
    # Remove empty subplots if needed
    for idx in range(len(keys), num_rows * num_cols):
        row = idx // num_cols
        col = idx % num_cols
        fig.delaxes(axes[row, col])

    # Adjust layout to prevent overlapping
    plt.tight_layout()
    plt.show()
# =============================================================================
#         # Get the keys and values from the dictionary
#         keys = list(key for key in relative_neighboring[system_chosen].keys(
#         ) if key.endswith(leaflet))
#         values = list(value for key, value in relative_neighboring[system_chosen].items(
#         ) if key.endswith(leaflet))
#         print(keys)
#         # Calculate the number of rows and columns for a square grid
#         num_plots = len(keys)
# # =============================================================================
# #         num_cols = 5
# #         num_rows = int(num_plots / num_cols)
# # =============================================================================
#         num_rows = int(np.sqrt(num_plots))
#         num_cols = int(np.ceil(num_plots / num_rows))
#         # Set up subplots in a square grid
#         fig, axes = plt.subplots(
#             nrows=num_rows, ncols=num_cols, figsize=(1.2*3*num_cols, 3*num_rows))
#
#         # Flatten the 2D array of subplots into a 1D array for easier indexing
#         axes = axes.flatten()
#
#         # Iterate through keys and values to plot on each subplot
#         for i, (key, value) in enumerate(zip(keys, values)):
#             ratio_l_x[system_chosen][key] = round(np.mean(value), 4)
#
#             # Plot errorbar on the current subplot
#             axes[i].errorbar(time, value)
#             axes[i].set_title(key)
#             # axes[i].yaxis.set_major_locator(major_locator)
#
#         # Remove empty subplots if needed
#         for j in range(i + 1, len(axes)):
#             fig.delaxes(axes[j])
#
#         # Adjust layout to prevent overlapping
#         plt.tight_layout()
# =============================================================================

    # Show the plots
    plt.show()

# =============================================================================
#     print(key, ratio_l_x[system_chosen][key], ratio_bulk[key[3:]])
#     enrichment_factor[key] = round(
#         ratio_l_x[system_chosen][key]/ratio_bulk[key[:3]+key[6:]], 2)
# =============================================================================
    print(system_chosen)
    for key, value in ratio_l_x[system_chosen].items():
        print(f"{key}: {value}")


# print("final enrichment factor for the last 10us: ")
# for key, value in enrichment_factor.items():
#     print(f"{key}: {value}")


# for k in relative_neighboring.keys():
#     print(len(relative_neighboring[k]))
#     # note golden ratio between x and y lengths
#     fig = plt.figure(figsize=(1.2*5, 5))
#     # plt.axhline(y=mean_small[k + '-4'], color='red', linestyle='-', zorder=2)
#     plt.errorbar(time1, relative_neighboring[k])

#     plt.legend(loc='upper left')
#     plt.show()

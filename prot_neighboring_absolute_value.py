#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 21:31:50 2024

@author: maryamma
"""

import io
import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
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


def filter_comments(line):
    return not line.startswith(('"', '&'))


directories = [
    # "/run/media/maryamma/One Touch/project_md/project_2/gromacs/step7/prot-const/neighboring/protein/"]

    "/run/media/maryamma/One Touch/project_md/project_2/gromacs/step7/no-posres/neighboring/protein/"]
systems = ['AA']
absolute_neighboring, relative_neighboring = {}, {}
colnames = ['time', 'number']
comment_chars = ['@', '#']
for dir, system_chosen in zip(directories, systems):
    absolute_neighboring[system_chosen], relative_neighboring[system_chosen] = {
    }, {}
    filename_list = sorted(f for f in os.listdir(
        dir) if f.endswith('upper-Protein.xvg'))
    # print(filename_list)
    for neighboring_file in filename_list:
        # print(neighboring_file)
        if neighboring_file.startswith('all'):
            # data_frame_all = pd.DataFrame()
            # print(new_dir)
            with open(dir + '/' + neighboring_file, 'r') as file:
                lines = [line.strip()
                         for line in file if not line.startswith(('#', '@'))]

            # Join the lines into a single string and create a DataFrame
            data_str = '\n'.join(lines)
            df = pd.read_csv(io.StringIO(data_str), sep='\s+', names=colnames)
            time_ref = df['time'].astype(float).to_numpy()/1000000
            neighboring_value_ref = df['number'].astype(float).to_numpy()
            # print(time_ref)
        else:
            with open(dir + '/' + neighboring_file, 'r') as file:

                lines = [line.strip()
                         for line in file if not line.startswith(('#', '@'))]

            # Join the lines into a single string and create a DataFrame
            data_str = '\n'.join(lines)
            df = pd.read_csv(io.StringIO(data_str), sep='\s+', names=colnames)
            # print(df)

            time = df['time'].astype(float).to_numpy()/1000000
            neighboring_value = df['number'].astype(float).to_numpy()
            relative = []
            for rel_num in range(0, len(neighboring_value)):
                relative.append(
                    np.round(neighboring_value[rel_num]/neighboring_value_ref[rel_num], 4))
            absolute_neighboring[system_chosen][neighboring_file[:-12]
                                                ] = neighboring_value
            relative_neighboring[system_chosen][neighboring_file[:-12]] = relative
            filename_list = sorted(f for f in os.listdir(
                dir) if f.endswith('lower-Protein.xvg'))
    # print(filename_list)
    for neighboring_file in filename_list:
        # print(neighboring_file)
        if neighboring_file.startswith('all'):
            # data_frame_all = pd.DataFrame()
            # print(new_dir)
            with open(dir + '/' + neighboring_file, 'r') as file:
                lines = [line.strip()
                         for line in file if not line.startswith(('#', '@'))]

            # Join the lines into a single string and create a DataFrame
            data_str = '\n'.join(lines)
            df = pd.read_csv(io.StringIO(data_str), sep='\s+', names=colnames)
            time_ref = df['time'].astype(float).to_numpy()/1000000
            neighboring_value_ref = df['number'].astype(float).to_numpy()
            # print(time_ref)
        else:
            with open(dir + '/' + neighboring_file, 'r') as file:

                lines = [line.strip()
                         for line in file if not line.startswith(('#', '@'))]

            # Join the lines into a single string and create a DataFrame
            data_str = '\n'.join(lines)
            df = pd.read_csv(io.StringIO(data_str), sep='\s+', names=colnames)
            # print(df)

            time = df['time'].astype(float).to_numpy()/1000000
            neighboring_value = df['number'].astype(float).to_numpy()
            relative = []
            for rel_num in range(0, len(neighboring_value)):
                relative.append(
                    np.round(neighboring_value[rel_num]/neighboring_value_ref[rel_num], 4))
            absolute_neighboring[system_chosen][neighboring_file[:-12]
                                                ] = neighboring_value
            relative_neighboring[system_chosen][neighboring_file[:-12]] = relative
    # print(relative_neighboring)
    for leaflet in ['upper', 'lower']:
        # Get the keys and values from the dictionary
        keys = list(key for key in relative_neighboring[system_chosen].keys(
        ) if key.endswith(leaflet))
        values = list(value for key, value in relative_neighboring[system_chosen].items(
        ) if key.endswith(leaflet))

        # Calculate the number of rows and columns for a square grid
        num_plots = len(keys)
        # print(num_plots)
        num_rows = int(np.sqrt(num_plots))
        num_cols = int(np.ceil(num_plots / num_rows))
        # Set up subplots in a square grid
        fig, axes = plt.subplots(
            nrows=num_rows, ncols=num_cols, sharex=True, figsize=(1.2*3*num_cols, 3*num_rows))

        # Flatten the 2D array of subplots into a 1D array for easier indexing
        axes = axes.flatten()

        # Iterate through keys and values to plot on each subplot
        for i, (key, value) in enumerate(zip(keys, values)):
            ratio_l_x[key] = round(np.mean(value), 4)

            # Plot errorbar on the current subplot
            axes[i].errorbar(time, value)
            axes[i].set_title(key)
            major_ticks = np.arange(round(min(value), 2)-0.01,
                                    round(max(value), 2)+0.01, 0.02)
            axes[i].set_yticks(major_ticks)    # Show the plots
            axes[i].set_ylim(round(min(value), 2)-0.002,
                             round(max(value), 2)+0.002)

        # Remove empty subplots if needed
        for j in range(i + 1, len(axes)):
            fig.delaxes(axes[j])

        # Adjust layout to prevent overlapping
        plt.tight_layout()
        max_diff = 0.2
        middle_table = (
            max(value) + min(value))/2
        # major_tick = np.array(max(value), min(value))
    plt.show()

# =============================================================================
#     print(key, ratio_l_x[key], ratio_bulk[key[3:]])
#     enrichment_factor[key] = round(
#         ratio_l_x[key]/ratio_bulk[key[:3]+key[6:]], 2)
# =============================================================================

for key, value in ratio_l_x.items():
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

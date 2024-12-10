#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 27 11:48:48 2023
This code derives the thickness of each system for different deformation rates
to check the interdigitation or change in thickness of the bilayer through 
calculating density profile of the phosphorous headgroups.
@author: maryamma
"""

import numpy as np
# from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import os
from natsort import natsorted
import pdb; pdb.set_trace()

def xvg_read(dir, var):
    temp_data = np.genfromtxt(
        (r for r in open(str(dir) + str(var)) if not r[0] in ('@', '#', '&')))
    time = temp_data.T[0]
    data = temp_data.T[1]
    return time, data


def strain_x(dir, var):
    time, box = [], []
    temp_box = np.genfromtxt(
        (r for r in open(dir + str(var) + '.xvg') if not r[0] in ('@', '#', '&')))
    for j in range(0, len(temp_box.T[0])):
        time.append((temp_box.T[0][j]))
        box.append(temp_box.T[1][j])
    return time, box


def find_two_maximum(arr):
    first_max = float('-inf')
    second_max = float('-inf')

    for num in arr:
        if num > first_max:
            second_max = first_max
            first_max = num
        elif num > second_max and num != first_max:
            second_max = num
    return first_max, second_max


string_x0 = [45.02, 45.23, 80.2, 41.76]

# choose between "axl", "large_prot", "plasma", "myelin", "node"
system = {"eq":"2fs", "deform":"deform/10-4", "eq-0.45":"deform/10-4/eq/0.45m"}
source_dir = "/run/media/maryamma/One Touch/project_md/project_2/gromacs"
for simulation, sub_dir in system.items():
    print(simulation)
    data_for_chosen_model = []
    directory = os.path.join(source_dir, sub_dir, 'density-prot/')
    # Replace with the desired file format (e.g., ".txt")
    desired_format = ".xvg"

    if os.path.exists(directory) and os.path.isdir(directory):
            # Filter and sort the files based on the specified part of their names
            files = natsorted(
                [f for f in os.listdir(directory) if os.path.isfile(
                    os.path.join(directory, f)) and f.endswith(desired_format)],
            )
    else:
            print(f"The directory '{directory}' does not exist.")

    all_tail_dist, x_timepoint = [], []
    for xvg_file in files:
            distance, density = xvg_read(directory,
                                         str(xvg_file))
            # Find peaks using find_peaks
            peaks, _ = find_peaks(density)

            # Sort the peaks by their y-values in descending order
            sorted_peaks = sorted(
                peaks, key=lambda distance: density[distance], reverse=True)

            # Select the two highest peaks
            two_highest_peaks = sorted_peaks[:2]

            # Plot the data and mark the peaks
            # plt.plot(distance, density)
            # plt.scatter(distance[two_highest_peaks], density[two_highest_peaks],
            #             c='red', marker='x', s=100, label='Two Highest Peaks')
            # plt.legend()
            # plt.show()

            # Print the x and y values of the two highest peaks
            # print("Peak 1 (distance, density):",
            #       distance[two_highest_peaks[0]], density[two_highest_peaks[0]])
            # print("Peak 2 (distance, density):",
            #       distance[two_highest_peaks[1]], density[two_highest_peaks[1]])
            # print(abs(distance[0]-distance[-1]),
            #       abs(distance[two_highest_peaks[1]]-distance[two_highest_peaks[0]]))
            tail_dist = min(abs(distance[0]-distance[-1])-abs(
                distance[two_highest_peaks[1]]-distance[two_highest_peaks[0]]), abs(
                distance[two_highest_peaks[1]]-distance[two_highest_peaks[0]]))
            all_tail_dist.append(round(tail_dist, 2))
            x_timepoint.append(xvg_file[5:-4])
            print(xvg_file[5:-4], round(tail_dist, 2))
    plt.scatter(x_timepoint, all_tail_dist)
    
    plt.ylabel('time(us)')
    plt.xlabel('bilayer_thickness (nm)')
    plt.title(simulation)
        # plt.savefig("/home/maryamma/project/project_md/paper1/density_plots/" +
        #            simulation + '.png')
    plt.show()

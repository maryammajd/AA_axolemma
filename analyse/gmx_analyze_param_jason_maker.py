#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  2 17:13:42 2023

@author: maryamma
"""

import os
import numpy as np
import json

csv_file = 'data.csv'

# from sklearn.linear_model import LinearRegression
# import matplotlib.pyplot as plt


def xvg_read(dir, var):
    temp_data = np.genfromtxt(
        (r for r in open(str(dir) + str(var) + '.xvg') if not r[0] in ('@', '#', '&')))
    time = temp_data.T[0]
    data = temp_data.T[1]
    return time, data


source_dir = "/run/media/maryamma/One Touch/project_md/project_2/analysis241205"

# out_put_data = [["system", "0.01-2-3-av", "0.01-3-4-ee", , "0.01-4-5-av", "0.01-5-6-ee", "0.02-2-3-av", "0.02-3-4-ee", "0.02-4-5-av", "0.02-5-6-ee"
#                 "0.03-2-3-av", "0.03-3-4-ee", "0.03-4-5-av", "0.02-5-6-ee" ]]


first_subdir_dirs = folder_list = [f for f in os.listdir(
    source_dir) if os.path.isdir(os.path.join(source_dir, f))]


directories=["eq", "deform/10-4/", "deform/10-4/eq/0.20", "deform/10-4/eq/0.35m", "deform/10-4/eq/0.45m", "deform/press75"]

simulations = ["0.01/", "0.02/", "0.03/"]
systems = ["eq", "deform", "0.2", "0.35", "0.45"]

output_for_chosen_model = {}

all_variables = ["sasa-protmemb", "gyrate-membprot", "hbnum-membprot"]
for var in all_variables:
    for system_name, dir in enumerate(directories):
        # print(systems[system_name])
        # print(systems[system_name])
        # for sims in simulations:
        path_to_sims = source_dir + dir + '/analyse/' # + sims
        file_list = os.listdir(path_to_sims)
        # print(path_to_fourth_dir)
        begin_time, end_time, average, st_err = [], [], [], []
        for time_separation, filename in enumerate(file_list):
            # Check if the file has the specified prefix
            if filename.endswith(f"-analyse-{var}.xvg"):
                # print(sims, filename)
                with open(path_to_sims + filename, 'r') as file:
                    # Loop through each line in the file
                    for line in file:
                        # Check if the search word is in the current line
                        if "-b " in line:
                            # print(line)
                            # Split the line into words using whitespace as a separator
                            words = line.split()
                            # Find the index of the search word in the list of words
                            index = words.index('-b')
                            # Print the word that follows the search word (if available)
                            if index < len(words) - 1:
                                # print(words[index - 1])
                                begin_time.append(
                                    int(words[index + 1])/1000000)
                        if "-e " in line:
                            # print(line)
                            # Split the line into words using whitespace as a separator
                            words = line.split()
                            # Find the index of the search word in the list of words
                            index = words.index('-e')
                            # Print the word that follows the search word (if available)
                            if index < len(words) - 1:
                                # print(words[index - 1])
                                end_time.append(
                                    int(words[index + 1])/1000000)
                        if "s0 " in line:
                            # print(line)
                            # Split the line into words using whitespace as a separator
                            words = line.split()
                            # Find the index of the search word in the list of words
                            index = words.index('"av')
                            # Print the word that follows the search word (if available)
                            if index < len(words) - 1:
                                # print(words[index + 1])
                                average.append(words[index + 1][:-2])
                        # else:
                        #     output_for_chosen_model.append(
                        #         'Error in performance finding')
                        if "s1 " in line:
                            # print(line)
                            # Split the line into words using whitespace as a separator
                            words = line.split()
                            # Find the index of the search word in the list of words
                            index = words.index('"ee')
                            # Print the word that follows the search word (if available)
                            if index < len(words) - 1:
                                # print(words[index - 1])
                                st_err.append(words[index + 1][:-2])
        # print(sims, begin_time, end_time, average, st_err)
        output_for_chosen_model[systems[system_name]] = {"begin_time": begin_time, "end_time": end_time,
                                                                        "average": average, "st_err": st_err}

    # print(output_for_chosen_model)

    json_file = f'/run/media/maryamma/One Touch/project_md/project_2/{var}_data_from_const_area.json'
    # Write the nested dictionary to a JSON file
    with open(json_file, 'w') as file:
        json.dump(output_for_chosen_model, file, indent=4)
    print(json_file + ' successfully built!')

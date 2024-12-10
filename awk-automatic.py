#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 15:24:21 2024

@author: maryamma
"""

import os
import pandas as pd
from io import StringIO
# dir = '/run/media/maryamma/One Touch/project_md/axl3/5.2/double-after25us/equilibrium/10us/neighbor/'

# dir = "/run/media/maryamma/One Touch/project_md/CG-axl-prot/small/node/eq/no-pos-res/neighbor/neighbor-all/"
# dir = "/run/media/maryamma/One Touch/project_md/CG-axl-prot/large/equilibrium/30us/neighbor/"
# dir = "/run/media/maryamma/One Touch/project_md/project_2/gromacs/step7/prot-const/200ns/neighboring/"
dir = '/run/media/maryamma/One Touch/project_md/project_2/gromacs/step7/no-posres//neighboring/'
colnames = ['time', 'number']
comment_chars = ['@', '#']


first_folder_list = [d for d in sorted(
    os.listdir(dir)) if os.path.isdir(os.path.join(dir, d))]
# first_folder_list = ['gl-up', 'pc-down', 'pe-down',
#                      'pe-up', 'pi-down', 'ps-down', 'sm-down', 'sm-up']
print(first_folder_list)
for first_folder in first_folder_list:
    second_folder_list = [d for d in sorted(os.listdir(dir + '/' + first_folder)) if os.path.isdir(
        os.path.join(dir + first_folder, d)) and not d.startswith('.')]
    # second_folder_list = ['pc-pc-down']
    for second_folder in second_folder_list:
        if not second_folder.startswith('chol'):
            try:
                print(second_folder)
                new_dir = dir + first_folder + '/' + second_folder
                filename_list = sorted(os.listdir(new_dir))
                data_frame_all = pd.DataFrame()
                os.chdir(new_dir)
                for filename in filename_list:
                    if filename.endswith(".xvg") and filename.startswith('neigh-'):
                        # print(new_dir + '/' + filename)
                        with open(new_dir + '/' + filename, 'r') as file:
                            lines = [line.strip() for line in file if not (
                                line.strip().startswith('@') or line.strip().startswith('#'))]
                        # Create a DataFrame from the filtered lines
                        df = pd.read_csv(StringIO('\n'.join(lines)),
                                         names=colnames, sep='\s+', engine='python')
                        data_frame_all = pd.concat(
                            [data_frame_all, df], axis=0)
            except FileNotFoundError:
                print(
                    f"Warning: {second_folder} is missing data. Skipping this file.")

                # Display the DataFrame
            result = data_frame_all.groupby(
                'time')['number'].mean().reset_index()
            # print(result)
            saved_data_dir = new_dir + '/' + second_folder + '.xvg'
            # print(saved_data_dir)
            result.to_csv(saved_data_dir, index=False)

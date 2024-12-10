#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 16:25:06 2024

@author: maryamma
"""

import numpy as np
import matplotlib.pyplot as plt

# dirs = ["/run/media/maryamma/One Touch/project_md/project_2/gromacs/step7/no-posres/",
#         "/run/media/maryamma/One Touch/project_md/project_2/gromacs/step7/no-posres/100-200gmx24/"]

# time1 = []
# msd1 = []
# absolute = []
# for i, directory in enumerate(dirs):
#     data1 = np.genfromtxt((r for r in open
#                            (directory + 'prot-in-memb.xvg')
#                            if not r[0] in ('@', '#', '&')))

#     time_temp = data1.T[0]/1000 + (i)*100
#     msd_temp = data1.T[1]
#     for i in range(0, len(msd_temp)):
#         time1.append(float(time_temp[i]))  # time in us
#         msd1.append(float(msd_temp[i]))
# combined_array = np.column_stack((time1, msd1))

# np.savetxt('/run/media/maryamma/One Touch/project_md/project_2/gromacs/step7/no-posres/prot-in-memb-stacked.xvg', combined_array, fmt='%d')

# plt.plot(time1, msd1)
# plt.show()
colors = ['#377eb8', '#ff7f00', '#4daf4a', '#f781bf', '#a65628', '#984ea3',
         '#999999', '#e41a1c', '#dede00']

dirs = ["/run/media/maryamma/One Touch/project_md/project_2/gromacs/step7/no-posres/",
        "/run/media/maryamma/One Touch/project_md/project_2/gromacs/step7/no-posres/100-200gmx24/", "/run/media/maryamma/One Touch/project_md/project_2/gromacs/2fs/"]
prot_rmsd = [0]
for i, directory in enumerate(dirs):
    data1 = np.genfromtxt((r for r in open
                           (directory + 'prot-in-memb.xvg')
                           if not r[0] in ('@', '#', '&')))

    time_temp = data1.T[0]/1000 # time in us
    msd_temp = data1.T[1]
    prot_rmsd = np.hstack((prot_rmsd, np.array(msd_temp)))
#     plt.plot(time_temp, msd_temp, color = colors[i] )
#     plt.axhline(y=np.mean(msd_temp), label = str(directory.split('/')[-2]), color = colors[i])
# # import pdb; pdb.set_trace()
# plt.axhline(y=np.mean(prot_rmsd), label = 'average', color = colors[i+1])
# plt.legend()
# plt.show()
print('prot_rmsd: ',np.mean(prot_rmsd))


dir_defs = ['/run/media/maryamma/One Touch/project_md/project_2/gromacs/deform/10-3/']
params = ['prot-in-memb', 'BB']
for i, param in enumerate(params):
    data1 = np.genfromtxt((r for r in open
                           (dir_defs[0] + param + '.xvg')
                           if not r[0] in ('@', '#', '&')))
    time_temp = data1.T[0]/1000 # time in us
    msd_temp = data1.T[1]
    plt.plot(time_temp, msd_temp, color = colors[i], label = param)
# import pdb; pdb.set_trace()
plt.axhline(y=np.mean(prot_rmsd), label = 'average', color = colors[i+1])
plt.axvline(x=15.8, label = 'protein movement', color = colors[i+2])
plt.legend()
plt.show()
step_size =100
params = ['ten']
for i, param in enumerate(params):
    data1 = np.genfromtxt((r for r in open
                           (dir_defs[0] + param + '.xvg')
                           if not r[0] in ('@', '#', '&')))
    time_temp, msd_temp = [], []
    for data_num in range(len(data1.T[1])):
        # import pdb; pdb.set_trace()
        if data1.T[0][data_num] % step_size == 0:
                time_temp.append(np.mean(data1.T[0][data_num:data_num+step_size])/1000) # time in us
                msd_temp.append(np.mean(data1.T[1][data_num:data_num+step_size]))
    plt.plot(time_temp, msd_temp, color = colors[i], label= param)
    plt.axvline(x=22.2, label = 'membrane poration', color = colors[i+1])
    plt.axvline(x=15.8, label = 'protein movement', color = colors[i+2])
    plt.legend()
    plt.show()

params = ['water-in-pocket', 'ion-in-pocket']
for i, param in enumerate(params):
    data1 = np.genfromtxt((r for r in open
                           (dir_defs[0] + param + '.xvg')
                           if not r[0] in ('@', '#', '&')))

    time_temp = data1.T[0]/1000 # time in us
    msd_temp = data1.T[1]
    plt.plot(time_temp, msd_temp, color = colors[i], label= param)
    plt.axvline(x=22.2, label = 'membrane poration', color = colors[i+1])
    plt.axvline(x=15.8, label = 'protein movement', color = colors[i+2])
    plt.legend()
    plt.show()
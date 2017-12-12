#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This program uses the MFP of phonons, given by ShengBTE, and calculates 
# lattice thermal conductivity when grain boundaries are introduced.
#
# Formula used:
#
# k_gb = k_int / (1 + L_mpf/L_gb)
#
# where 
# k_gb  - lattice thermal conductivity with grain boundaries
# k_int - intrinsic lattice thermal conductivity given by ShengBTE
# L_mfp - phonon mean free path
# L_gb  - size of grain boundaries

import numpy as np
import sys
import os

L_gb = float(sys.argv[1]) # in [m]

list_of_folders =[x[0] for x in os.walk(".")]

final_data={}


for folder in range(1,len(list_of_folders)):

	file_path = str(list_of_folders[folder]) + '/BTE.cumulative_kappa_scalar'

	L_mfp, k_int = np.loadtxt(fname=file_path, unpack=True)
        temperature = ''
	for i in range(3, (len(list_of_folders[folder])-1)):
     		temperature += str(list_of_folders[folder][i])

	# contribution of each data point to k_int
	k_int_cont = np.empty([len(k_int)])

	for i in range(0, len(k_int)):
		if i == 0:
			k_int_cont[i] = k_int[i] - 0.0
        	else:
			k_int_cont[i] = k_int[i] - k_int[i-1]	

	# apply gb formula to each data point
	k_gb = np.empty([len(k_int_cont)])

	for i in range(0, len(k_int_cont)):
		k_gb[i] = k_int_cont[i]/(1 + (L_mfp[i]*1e-9)/L_gb) # convert L_mfp from [nm] to [m]

	k_gb_cumul = np.sum(k_gb)
	final_data[int(temperature)] = k_gb_cumul

	

final_data = sorted(final_data.items())
print '# L_gb = ' + '%s' %str(L_gb) + ' m'
print '# Temp[K] kappa_with_gb[W/m*K]' 
for key in final_data:
        
	print key[0], key[1]

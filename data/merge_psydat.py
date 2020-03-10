#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A script to merge two or more .psydat files.

For example if subject numbers were entered incorrectly, \
a subject's data might be spread across two .psydat files. \
These then need to be exported into the same .csv results file.
"""

from psychopy import misc


#%% Parameters

# Files to be merged.
filenames = ['A14.psydat', 'K14A14.psydat']

# Correct subject ID under which to store all files.
correct_ID = 'A14'


#%% Main loop

for i, f in enumerate(filenames):
    
    # Load in the .psydat file.
    psydata = misc.fromFile(f)
    
    # Change the subject name.
    psydata.extraInfo.update({'subject': correct_ID})
    
    # Export to csv.
    # Write the header line only for the first file.
    psydata.saveAsWideText(correct_ID,
                           delim=',',
                           matrixOnly=i>0,
                           appendFile=i>0,
                           encoding='utf-8')

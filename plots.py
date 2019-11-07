#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Visualize data from GestureSpeededFragments experiment.
"""

import os
import re
import webbrowser

from matplotlib import pyplot
import pandas
import plotnine


#%% Parameters

# Files
data_dir = 'data'
filename_pattern = r'\w\d{2}\.csv'
plot_dir = 'plots'

# Exclusion criteria
RT_cutoff = 5

# Plots
file_format = '.svg'
img_width = 6
img_height = 4


#%% Functions

def save_plot(filename, plot, width=img_width, height=img_height):
    filename = os.path.join(plot_dir, filename+file_format)
    plot.save(filename, width=width, height=height)
    webbrowser.open(filename)


#%% Load data

filenames = [f for f in os.listdir(data_dir) if re.fullmatch(filename_pattern, f)]
filenames = [os.path.join(data_dir, f) for f in filenames]

data = pandas.concat((pandas.read_csv(f) for f in filenames), sort=False)

data.rename(columns={'correct':'response'}, inplace=True)
data.replace({'response':{True:'correct', False:'incorrect'}}, inplace=True)

print(data.head())


#%% RT histograms

rt_hist = (plotnine.ggplot(plotnine.aes(x='RT'), data) +
           plotnine.labs(x='RT (s)'))
save_plot('RT_histogram_full',
          rt_hist + plotnine.geom_histogram(binwidth=0.1))

rt_hist.data = data[data['RT'] < RT_cutoff]

save_plot('RT_histogram',
          rt_hist + plotnine.geom_histogram(binwidth=0.1))

rt_hist_response = (rt_hist +
                    plotnine.aes(fill='response') +
                    plotnine.scale_fill_manual(['green', 'red']) +
                    plotnine.geom_histogram(alpha=0.5, position=plotnine.position_identity()))
save_plot('RT_histogram_by_response',
          rt_hist_response)

save_plot('RT_histogram_by_response_subjects',
          rt_hist_response + plotnine.facet_wrap('subject'),
          width=9, height=6)

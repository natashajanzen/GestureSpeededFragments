#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GestureSpeededFragments experiment.
"""

import glob
import os
import random
import statistics

from matplotlib import pyplot
import pandas
import plotnine
from psychopy import visual, core, data, event, tools


#%% Parameters

# Files.
example_video = 'baby_PL_copy.mp4'
trials_filename = 'mainTrials.xlsx'
test_trials_filename = 'mainTrials_test.xlsx'

# Window size.
# (Needs to be at least as large as the videos to avoid cropping them.)
window_size = (1280, 720)

# Colors.
colors = {'background': (0, 0, 0),
          'text': (1, 1, 1),
          'correct': (-1, 1, -1),
          'incorrect': (1, -1, -1)}

# Timing.
short_wait = 0.25
feedback_duration = 1.0
video_end_pause = 0.5


#%% Functions

def instructions(filename):
    """
    Display an onscreen message from a text file.
    """
    filename = os.path.join('text', filename)
    text = visual.TextStim(win,
                           text=open(filename, encoding='utf-8').read(),
                           color=colors['text'],
                           wrapWidth=1.95)
    text.draw()
    win.flip()
    event.waitKeys()
    win.flip()
    core.wait(short_wait)


#%% Data setup

# Get subject ID.
existing_files = glob.glob(os.path.join('data', '*.psydat'))
existing_ids = [x.split(os.path.sep)[-1].split('.')[0] for x in existing_files]
print('Subject IDs already in use: {}'.format(existing_ids))
subject_id = input('Subject ID: ').strip()

# Allocate a file name for the subject.
subject_filename = os.path.join('data', subject_id + '.psydat')

# Get trials for an existing subject (or generate new ones).
if os.path.exists(subject_filename):
    trials = tools.filetools.fromFile(subject_filename)
    if trials.finished:
        msg = "Subject '{}' has already completed the study."
        raise ValueError(msg.format(subject_id))
else:
    
    # Decide on test mode.
    test_mode = input('Test mode? (y/n): ').strip().lower()[:1]
    if test_mode not in ['y', 'n']:
        raise ValueError("Answer must be one of 'y' or 'n'.")
    if test_mode == 'y':
        trial_types = data.importConditions(test_trials_filename)
    else:
        trial_types = data.importConditions(trials_filename)
    
    # Get the desired order of conditions.
    order = input('Order (S or G): ').strip().lower()
    if order not in ['s', 'g']:
        raise ValueError("Order must be one of 'S' or 'G'.")
    
    # Shuffle and sort by condition.
    random.shuffle(trial_types)
    trial_types.sort(key=lambda x: x['condition'], reverse=order == 's')
    trials = data.TrialHandler(trial_types,
                               nReps=1,
                               method='sequential',
                               extraInfo={'subject': subject_id})


#%% Psychopy setup

# Keys.
response_keys = ['a', 'e', 'i', 'o', 'u']
quit_key = 'q'

# Timer.
timer = core.Clock()

# Window.
win = visual.Window(size=window_size, color=colors['background'])
visual.TextStim(win, text='loading...', color=colors['text']).draw()
win.flip()

# Text stimulus.
fragment = visual.TextStim(win)

# Video stimulus.
video = visual.MovieStim3(win, example_video)


#%% Intro

instructions('intro.txt')


#%% Practice


#%% Main loop

for t in trials:
    
    # Play the gesture video.
    video.loadMovie(t['gestures'])
    video.play()
    while video.status != visual.FINISHED:
        video.draw()
        win.flip()
        core.wait(0.001)
    core.wait(video_end_pause)
    
    # Show the fragment.
    fragment.color = colors['text']
    fragment.text = t['target']
    fragment.draw()
    win.flip()
    timer.reset()
    
    # Wait for a response.
    response = event.waitKeys(keyList=response_keys + [quit_key],
                              timeStamped=timer)
    key = response[0][0]
    rt = response[0][1]
    correct = key == t['corrAns']
    
    # Store response.
    trials.addData('RT', rt)
    trials.addData('answer', key)
    trials.addData('correct', correct)
    
    # Quit if requested.
    if key == quit_key:
        break
    
    # Feedback.
    if not correct:
        fragment.text = t['target'].replace('_', key)
        fragment.color = colors['incorrect']
        fragment.draw()
        win.flip()
        core.wait(feedback_duration)
    fragment.text = t['target'].replace('_', t['corrAns'])
    fragment.color = colors['correct']
    fragment.draw()
    win.flip()
    core.wait(feedback_duration)
    
    # Pause between trials.
    win.flip()
    core.wait(short_wait)
    
    # Break between blocks.
    next_trial = trials.getFutureTrial(1)
    if next_trial and (t['condition'] != next_trial['condition']):
        break


#%% End

instructions('end.txt')
win.close()


#%% Save and summarize

# Save trials whether the session was completed or not.
# These can be reloaded later to finish the session.
trials.saveAsPickle(subject_filename, fileCollisionMethod='overwrite')

# If the session was completed all the way to the end,
# save all the data as a spreadsheet and show some summaries.
if trials.finished:
    
    # Save.
    results_filename = os.path.join('data', subject_id + '.csv')
    results = trials.saveAsWideText(results_filename,
                                    fileCollisionMethod='overwrite',
                                    encoding='utf-8')
    
    # Plot.
    fig = (plotnine.ggplot(plotnine.aes(x='RT', color='correct', fill='correct'), results) +
           plotnine.geom_histogram(alpha=0.5, position=plotnine.position_identity()) +
           plotnine.facet_wrap('condition', nrow=2, labeller='label_both') +
           plotnine.labs(x='RT (s)'))
    fig.draw()
    pyplot.show()
    
    # Summarize.
    summary_accuracy = pandas.crosstab(results['condition'], results['correct'],
                                       dropna=False,
                                       normalize='index')
    try:
        summary_rt = results.groupby(['condition', 'correct']).agg({'RT': [statistics.mean, statistics.stdev]})
    except statistics.StatisticsError:
        summary_rt = results.groupby(['condition', 'correct']).agg({'RT': [statistics.mean]})
    msg = '\n#### Summary ####\n\n{}\n\n{}\n\n#################\n'
    print(msg.format(summary_accuracy, summary_rt))

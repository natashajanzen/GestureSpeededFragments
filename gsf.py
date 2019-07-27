#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GestureSpeededFragments experiment.
"""

import glob
import os
import webbrowser

import numpy
import pandas
from psychopy import visual, core, data, event, tools


#%% Parameters

# Files.
file_encoding = 'utf-8'
trials_filename = 'mainTrials.xlsx'

# Timing.
short_wait = 0.25
feedback_duration = 1.0

# Colors.
colors = {'background': (0, 0, 0),
          'text': (1, 1, 1),
          'correct': (-1, 1, -1),
          'incorrect': (1, -1, -1)}


#%% Functions

def instructions(filename):
    """
    Display an onscreen message from a text file.
    """
    filename = os.path.join('text', filename)
    msg = open(filename, encoding=file_encoding).read()
    text = visual.TextStim(win, text=msg,
                           color=colors['text'],
                           wrapWidth=1.95)
    text.draw()
    win.flip()
    event.waitKeys()
    win.flip()
    core.wait(short_wait)


#%% Trial data

# Print a list of subject ids already used.
existing_files = glob.glob(os.path.join('data', '*.psydat'))
existing_ids = [x.split(os.path.sep)[-1].split('.')[0] for x in existing_files]
print('Subject IDs already in use: {}'.format(existing_ids))

# Experimenter input at the console.
subject_id = input('Subject ID: ')

# Allocate a file name for the subject.
subject_filename = os.path.join('data', subject_id)

# Either get trials for existing subject, or create new ones.
try:
    trials = tools.filetools.fromFile(subject_filename + '.psydat')
except FileNotFoundError:
    trials = data.TrialHandler(data.importConditions(trials_filename),
                               nReps=1,
                               method='random',
                               extraInfo={'subject': subject_id})


#%% Psychopy setup

# Keys.
response_keys = ['a', 'e', 'i', 'o', 'u']
quit_key = 'q'

# Timer.
timer = core.Clock()

# Window.
win = visual.Window(color=colors['background'])

# Stimuli.
fragment = visual.TextStim(win)


#%% Intro

instructions('intro.txt')


#%% Practice


#%% Main loop

for t in trials:
    
    # Play the gesture video.
    
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


#%% End

instructions('end.txt')
win.close()


#%% Save and summarize

trials.saveAsPickle(subject_filename, fileCollisionMethod='overwrite')

if trials.finished:
    
    # Save.
    results_filename = os.path.join('data', subject_id + '.csv')
    results = trials.saveAsWideText(results_filename,
                                    encoding=file_encoding)
    
    # Summaries.
    summary_accuracy = pandas.crosstab(results['condition'], results['correct'],
                                       normalize=True)
    print(summary_accuracy)
    summary_rt = results.groupby(['condition', 'correct']).agg({'RT': [numpy.mean, numpy.std]})
    print(summary_rt)
    
    # Open spreadsheet.
    webbrowser.open(results_filename)

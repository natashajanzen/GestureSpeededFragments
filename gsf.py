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
example_video = 'baby_PL_copy.mp4'

# Timing.
short_wait = 0.25
feedback_duration = 1.0
video_end_pause = 0.5

# Colors.
colors = {'background': (0, 0, 0),
          'text': (1, 1, 1),
          'correct': (-1, 1, -1),
          'incorrect': (1, -1, -1)}

# Window size.
# (Needs to be at least as large as the videos to avoid cropping them.)
window_size = (1280, 720)


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

# Either get trials for an existing subject, or create new ones.
try:
    trials = tools.filetools.fromFile(subject_filename + '.psydat')
except FileNotFoundError:
    trials = data.TrialHandler2(data.importConditions(trials_filename),
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


#%% End

instructions('end.txt')
win.close()


#%% Save and summarize

# Save trials whether the session was completed or not.
# These can be reloaded later to finish the session.
trials.saveAsPickle(subject_filename, fileCollisionMethod='overwrite')

# If the session was completed all the way to the end,
# save all the data as a spreadsheet and print some summaries.
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

# GestureSpeededFragments

[baby_PL_copy.mp4](baby_PL_copy.mp4)  
Example gesture video. Also used in the experiment as a 'dummy' first loaded video.

[gsf.py](gsf.py)  
A Python script to run the experiment, using Psychopy.

[mainTrials.xlsx](mainTrials.xlsx)  
Spreadsheet of trial types.

[requirements.txt](requirements.txt)  
List of Python package versions used when developing the experiment. As produced by `pip freeze`. In particular note that Psychopy currently requires an older version of pyglet (1.3) than the latest (1.4), as per [this issue](https://github.com/psychopy/psychopy/issues/2518). You can force install the older version with `pip install 'pyglet<1.4' --force-reinstall`.

[data](data)  
Data collected in the experiment is saved here. *.psydat* files store Psychopy TrialHandler objects. These are saved even if the subject does not complete the experiment. *.csv* files store results from completed runs of the experiment.

[extras](extras)  
Miscellaneous additional files.

[gestures](gestures)  
*.mp4* video files with the gestures. Shown on screen during the experiment.

[text](text)  
Text files of onscreen instructions.
#!/bin/bash

# Generate slowed versions of the gesture videos:

# Get the original videos (all *.mp4 files in the current directory).
# Slow them by a factor of 2 and a factor of 3 (using ffmpeg).
# Put the new videos in correspondingly-named subdirectories.

# For a factor of 2 and of 3...
for SLOWFACTOR in 2 3; do

    # make a new directory for the slowed videos,
    NEWDIRNAME="slow_$SLOWFACTOR"
    mkdir -p $NEWDIRNAME

    # then for every .mp4 file...
    for FILENAME in *.mp4; do

        # go into the new directory,
        NEWFILENAME="$NEWDIRNAME/$FILENAME"
        echo "$FILENAME -> $NEWFILENAME ..."

        # and save there a slowed down version (using the ffmpeg program).
        ffmpeg -i $FILENAME -filter:v "setpts=$SLOWFACTOR*PTS" $NEWFILENAME

    done

done

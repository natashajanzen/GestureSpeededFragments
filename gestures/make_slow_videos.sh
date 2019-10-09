#!/bin/bash

# Generate slowed versions of the gesture videos.
# Get the original videos (all *.mp4 files in the current directory).
# Slow them by a factor of 2 and a factor of 3 (using ffmpeg).
# Put the new videos in correspondingly-named directories.

for SLOWFACTOR in 2 3; do
  NEWDIRNAME="slow_$SLOWFACTOR"
  mkdir -p $NEWDIRNAME
  for FILENAME in *.mp4; do
    NEWFILENAME="$NEWDIRNAME/$FILENAME"
    echo "$FILENAME -> $NEWFILENAME ..."
    ffmpeg -i $FILENAME -filter:v "setpts=$SLOWFACTOR*PTS" $NEWFILENAME
  done
done


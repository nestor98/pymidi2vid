"""
Mezcla dos videos
"""
import sys
import os
import numpy as np

# import matplotlib
# matplotlib.rcParams['backend'] = "Qt4Agg"

import matplotlib.pyplot as plt

import argparse
from moviepy.editor import AudioFileClip,VideoFileClip,CompositeVideoClip



def main(args):
    v = VideoFileClip(args.video)
    a = AudioFileClip(args.audio)
    v.audio = a
    v.write_videofile(args.output,fps=25, threads=11)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--video', help='video file', type=str, default="original/escala.mp4")
    parser.add_argument('-a', '--audio', help='audio file', type=str, default="original/escala.mp4")
    parser.add_argument('-o', '--output', help='output video file', type=str, default="")

    args = parser.parse_args()
    main(args)

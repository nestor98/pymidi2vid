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
from moviepy.editor import AudioFileClip,VideoFileClip,CompositeVideoClip,afx



def main(args):
    guitar = VideoFileClip(args.guitar).resize(args.quality).fx(afx.audio_normalize).subclip(0,"0:2:28")
    bass = (
        VideoFileClip(args.bass).resize([s/2 for s in guitar.size])
        .set_position((0.5,0.5),relative=True)
        .volumex(2)
        .fx(afx.audio_normalize)
    )
    r = CompositeVideoClip([guitar,bass], size = guitar.size)
    r.write_videofile(args.output,fps=25, threads=11)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-g', '--guitar', help='guitar video file', type=str, default="original/escala.mp4")
    parser.add_argument('-b', '--bass', help='bass video file', type=str, default="original/escala.mp4")
    parser.add_argument('-o', '--output', help='output video file', type=str, default="")
    parser.add_argument('-q', '--quality', help='reduce quality (e.g. 0.5)', type=float, default=1)

    args = parser.parse_args()
    main(args)

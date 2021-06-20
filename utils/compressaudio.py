"""
Yo que se ya
"""
import sys
import os

import argparse
from moviepy.editor import AudioFileClip, VideoFileClip


from pysndfx import AudioEffectsChain



def to_wav(input):
    AudioFileClip(input+'.mp4').write_audiofile(input+".wav")



def main(args):


    fx = (
        AudioEffectsChain()
        .lowpass(1200)
        # .compand(attack =0.01, decay = 0.1,soft_knee=6,db_from=-20.0, db_to=-30.0)#(attack =0.01, decay = 0.05, soft_knee=200)#,db_from=-0.0, db_to=-2000.0)
        # .reverb()
        # .phaser()
        # .delay()
        # .lowshelf()
    )

    mp4 = os.path.splitext(args.input)[0]
    print("Converting to wav...")
    to_wav(mp4)
    fx(mp4+".wav", mp4+"-audiofix.wav")


    audio = AudioFileClip(mp4+"-audiofix.wav")
    video = VideoFileClip(mp4+".mp4")
    video.audio = audio
    video.write_videofile(mp4+"-audiofix.mp4",fps=25, threads=11)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help='Input video file', type=str, default="original/escala.mp4")
    parser.add_argument('-w', '--weight', help='Weight of the sound to be detected (0 to 1)', type=float, default=0.7)
    parser.add_argument('-o', '--output', help='output csv file', type=str, default="")

    args = parser.parse_args()
    main(args)

"""
Yo que se ya
"""
import sys
import os
import numpy as np

# import matplotlib
# matplotlib.rcParams['backend'] = "Qt4Agg"

import matplotlib.pyplot as plt

import argparse
from moviepy.editor import AudioFileClip

from pyAudioAnalysis import audioBasicIO

#from pyAudioAnalysis import audioSegmentation as pas
# silenceRemovalWrapper

# https://stackoverflow.com/a/64914123
def to_wav(input):
    AudioFileClip(input+'.mp4').write_audiofile(input+".wav")


def time2idx(fs, time):
    return int(time * fs) #/ len(x)

def idx2time(fs, i):
    return i / fs


def main(args):

    if not os.path.isfile(args.input):
        raise Exception("Input audio file not found!")

    mp4 = os.path.splitext(args.input)[0]
    print("Converting to wav...")
    to_wav(mp4)
    # fx(mp4+".wav", mp4+"-audiofix.wav")
    [fs, x] = audioBasicIO.read_audio_file(mp4+".wav")
    x = audioBasicIO.stereo_to_mono(x)
    print("fs:", fs, "x:", x, len(x), sep="\n")

    t = np.linspace(0, len(x) / fs, num=len(x))

    #
    # for t in [5,10,15,20,30]:
    #     i = time2idx(fs,t)
    #     print(t, " --idx-> ", i, idx2time(fs,t))
    #     closest = closest_zero(x,fs,i,int(time2idx(fs,0.05)))
    #     print("closest zero:", closest, "t:", idx2time(fs,closest), x[i], '->',x[closest])



    fig = plt.figure(1)
    plt.title("Signal Wave...")
    plt.plot(t,x)#, marker=".")
    # for time in times:
    #     plt.axvline(x=time, color='r')
    plt.show()


    # plt.savefig('wave.png')

    # plt.close()



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help='Input audio file', type=str, default="original/escala.mp4")
    parser.add_argument('-t', '--timestamps_file', help='Input timestamps file', type=str, default="")
    parser.add_argument('-o', '--output', help='output csv file', type=str, default="")

    args = parser.parse_args()
    main(args)

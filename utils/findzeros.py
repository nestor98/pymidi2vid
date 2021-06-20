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

def closest_zero(x, fs, i):
    """ Returns the closest zero to <time>"""
    min = 1000000
    j = -1
    last = abs(x[j])
    lowering = False
    for j in range(i, i):
        val = abs(x[j])
        if val < last:
            lowering = True
        elif lowering and val > last: # stop
            break
        if val < min:
            min = x[j]
            jmin = j
        last = val
    return j

def closest_zero(x, fs, i, rang):
    """ Returns the closest zero to <time>"""
    min = abs(x[i])
    jmin = -1
    for j in range(i, i+rang):
        val = abs(x[j])
        if val < min:
            min = val
            jmin = j
    return jmin

def time2idx(fs, time):
    return int(time * fs) #/ len(x)

def idx2time(fs, i):
    return i / fs


def main(args):

    if not os.path.isfile(args.input):
        raise Exception("Input audio file not found!")

    [fs, x] = audioBasicIO.read_audio_file(args.input)
    x = audioBasicIO.stereo_to_mono(x)
    print("fs:", fs, "x:", x, len(x), sep="\n")
    zeros = [i for i in range(len(x)) if x[i]==0]
    print(zeros)
    # for s in segmentos:
    #     print(s)

    times = []

    if args.timestamps_file != "":
        with open(args.output, 'w') as out: # output file
            with open(args.timestamps_file, 'r') as f: # input file
                for l in f:
                    l = l.split(";") # to list
                    if len(l) > 1:
                        t = float(l[1])+0.15 # time
                        i = time2idx(fs,t) # to index
                        closest = closest_zero(x,fs,i,int(time2idx(fs,0.2))) # find closest 0 at 0.05 s max
                        t = idx2time(fs,closest) # new t
                        times+=[t]
                        fixed = [l[0]] + [str(t)] + l[2:] # "fixed" time list
                        fixed = ";".join(fixed) # as str
                        out.write(fixed) # save to output file

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
    for time in times:
        plt.axvline(x=time, color='r')
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

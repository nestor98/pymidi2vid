"""
Yo que se ya
"""
import sys
import os

import argparse
from moviepy.editor import AudioFileClip
from pyAudioAnalysis import audioAnalysis as pa
from pyAudioAnalysis import audioSegmentation as aS
from pyAudioAnalysis import audioBasicIO

#from pyAudioAnalysis import audioSegmentation as pas
# silenceRemovalWrapper

# https://stackoverflow.com/a/64914123
def to_wav(input):
    AudioFileClip(input+'.mp4').write_audiofile(input+".wav")



def mySilenceRemovalWrapper(inputFile, smoothingWindow, weight):
    if not os.path.isfile(inputFile):
        raise Exception("Input audio file not found!")

    [fs, x] = audioBasicIO.read_audio_file(inputFile)
    segmentLimits = aS.silence_removal(x, fs, 0.05, 0.05, smoothingWindow, weight, False)
    # for i, s in enumerate(segmentLimits):
    #     strOut = "{0:s}_{1:.3f}-{2:.3f}.wav".format(inputFile[0:-4], s[0], s[1])
    #     wavfile.write(strOut, fs, x[int(fs * s[0]):int(fs * s[1])])
    return segmentLimits



def procesar(wav, window, weight):
    limits = mySilenceRemovalWrapper(wav, smoothingWindow=window, weight=weight)

    # silence_removal(signal, sampling_rate, st_win, st_step, smooth_window=0.5,
    #                     weight=0.5, plot=False)
    return limits


def main(args):
    mp4 = os.path.splitext(args.input)[0]
    print("Converting to wav...")
    to_wav(mp4)
    print("Segmentation... ", end="")
    segmentos = procesar(mp4+".wav", args.smoothing_window, args.weight)
    #print("Segmented:")
    # output file:
    f_name = mp4 + ".csv" if args.output == "" else args.output
    print("Done, saving timestamps to csv:", f_name)
    note = args.lowest_note
    with open(f_name, 'w') as f:
        for s in segmentos:
            f.write(str(note) + ";" + str(s[0]) + ";" + str(s[1]) + "\n")
            note += 1

    # for s in segmentos:
    #     print(s)




if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help='Input video file', type=str, default="original/escala.mp4")
    parser.add_argument('-l', '--lowest_note', help='Lowest note in the video', type=int, default=52)
    #parser.add_argument('-h', '--highest_note', help='Highest note in the video', type=int, default=98)
    parser.add_argument('-s', '--smoothing_window', help='length of the segments detected (s)', type=float, default=1)
    parser.add_argument('-w', '--weight', help='Weight of the sound to be detected (0 to 1)', type=float, default=0.7)
    parser.add_argument('-o', '--output', help='output csv file', type=str, default="")

    args = parser.parse_args()
    main(args)

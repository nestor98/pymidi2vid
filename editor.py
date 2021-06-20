"""
Yo que se ya
"""

import argparse
import mido
import logging
from timeit import default_timer as timer

from video import Video

# from moviepy.editor import *

DEBUG = True

def print_d(msg):
    if DEBUG:
        print(msg)

def maxSymNotes(notes):
    curr = max = 0
    for note in notes:
        if note[2] == 0:
            curr+=1
            if curr > max:
                max = curr
        else:
            curr = 0
    return max



def keep_only_highest(notes):

    curr = 0
    highest = -1
    highest_t = 0
    h_v = 0
    new = []
    for (note, vel, t) in notes:
        if vel == 0: #stop note
            new += [(note, vel, t)]
            # v.addNote(note, vel, t)
        if t == 0:
            highest = max(highest, note)
            highest_t = t
            h_v = vel
        else:
            curr += t
            # print("now at: ", curr)
            if highest != -1:
                # print("adding:", highest)
                new += [(highest, h_v, highest_t)]
                highest = -1
                highest_t = 0
                h_v = 0
    return new

def misirlou(low = 52, c = 4, duration = 0.05, vel=10):
    """ Returns a sequence like misirlou kinda """
    notes = ([low+0]*c*3 + [low+1]*c + [low+4]*c*2 + [low+5]*c*2 +
            [low+7]*c*3 + [low+8]*c + [low+11]*c*2 + [low+8]*c*2 +
            [low+7]*c*8)
    notes = (notes*2 +
            [low+8]*c*2 + [low+7]*c + [low+8]*c + [low+7]*c*2 + [low+5]*c*2 +
            [low+7]*c*2 + [low+5]*c + [low+7]*c + [low+5]*c*2 + [low+4]*c + [low+1]*c +
            [low+4]*c*8 +
            [low+7]*c*2 + [low+5]*c + [low+7]*c + [low+5]*c*2 + [low+4]*c*2 +
            [low+5]*c*2 + [low+4]*c + [low+5]*c + [low+4]*c*2 + [low+1]*c*2 +
            [low+0]*c*8)
    msgs = []
    print(notes)
    # notes = [note for n in notes  for note in n]
    for note in notes:
        msgs += [(note, vel, 0)] # start
        msgs += [(note, 0, duration)]   # stop duration secs later
    return msgs


def chromatic(lowest=52, highest=76, duration = 0.5, vel=10):
    """ chromatic scale from from lowest to highest """
    notes = [n for n in range(lowest, highest+1)]
    msgs = []
    # print(notes)
    # notes = [note for n in notes  for note in n]
    for note in notes:
        msgs += [(note, vel, 0)] # start
        msgs += [(note, 0, duration)]   # stop duration secs later
    return msgs


def octaves(lowest=52, highest=76, duration = 0.5, vel=10):
    """ each octave of each note, lowest to highest """
    notes = []
    for n in range(12):
        note = lowest + n
        while note <= highest:
            notes += [note]
            note +=12
    msgs = []
    # print(notes)
    # notes = [note for n in notes  for note in n]
    for note in notes:
        msgs += [(note, vel, 0)] # start
        msgs += [(note, 0, duration)]   # stop duration secs later
    return msgs


def merge_parse(mid, ignore = [6,7,8, 10, 11, 12]):
    """
    Merges all tracks then returns the notes as [(notecode, vel, t)].
    Tempo changes are translated to (-1,tempo,t), unknown messages to (-2,0,t)
    """
    tracks = []

    for i, track in enumerate(mid.tracks):
        print_d('Track {}: {}'.format(i, track.name))
        if i not in ignore:
            tracks += [track]
        else: # fake track only to keep times
            print('(ignoring this one)')
            newtrack = mido.MidiTrack()
            for msg in track:
                newtrack.append(mido.Message('program_change', program=0, time=msg.time))
            tracks += [newtrack]
    track = mido.merge_tracks(tracks)

    notes = []

    bpm = 120 # default
    tempo = 500000

    total_ticks = 0
    for msg in track:
        total_ticks += msg.time
        if msg.is_meta:
            # print(msg)
            if msg.type == 'set_tempo':
                print('tempo msg:',msg)
                notes += [(-1,  msg.tempo * args.slow, msg.time)]
                if tempo == 500000:
                    tempo = msg.tempo * args.slow # only the first one
            else:
                # print('unknown meta msg:', msg)
                notes += [(-2, 0, msg.time)] # only add time
        elif msg.type == 'note_off': # convert to note_on with vel = 0
            notes += [(msg.note, 0, msg.time)]#mido.tick2second(msg.time, mid.ticks_per_beat, tempo))]
        elif msg.type == 'note_on':
            notes += [(msg.note, msg.velocity, msg.time)]# mido.tick2second(msg.time, mid.ticks_per_beat, tempo))]
        else:
            # print('unknown msg:', msg)
            notes += [(-2, 0, msg.time)]

    return notes, tempo, total_ticks

def print_notes(notes):
    all_notes = {n[0] for n in notes if n[0]>=0} # set, remove repetitions
    for note in sorted(all_notes): # sorted
        print(note)


def parseMidi(mid, args):
    """ returns the notes as [(notecode, vel, t)] """
    notes = []

    bpm = 120 # default
    tempo = 500000


    total_ticks = 0
    for i, track in enumerate(mid.tracks):
        print_d('Track {}: {}'.format(i, track.name))

        for msg in track:
            total_ticks += msg.time
            if i != args.track:
                break # TODO: this is bad!!
            if msg.is_meta:
                # print(msg)
                if msg.type == 'set_tempo':
                    print('tempo msg:',msg)
                    notes += [(-1,  msg.tempo * args.slow, msg.time)]
                    if tempo == 500000:
                        tempo = msg.tempo * args.slow # only the first one
                    # tempos += 1
                    # tempo = args.slow * msg.tempo
                    # bpm = mido.tempo2bpm(tempo)
                    # print("bpm: ", bpm)
                else:
                    # print('unknown meta msg:', msg)
                    notes += [(-2, 0, msg.time)]


            elif msg.type == 'note_off':
                notes += [(msg.note, 0, msg.time)]#mido.tick2second(msg.time, mid.ticks_per_beat, tempo))]
            elif msg.type == 'note_on':
                notes += [(msg.note, msg.velocity, msg.time)]# mido.tick2second(msg.time, mid.ticks_per_beat, tempo))]
            else:
                # print('unknown msg:', msg)
                notes += [(-2, 0, msg.time)]
                # video.addNote(msg.note, msg.velocity, mido.tick2second(msg.time))
                # print(msg, msg.type)
                # print("note: ", msg.note, " vel: ", msg.velocity, "t: ", msg.time)
    # print('tempo changes:', tempos)
    return notes, tempo, total_ticks


def main(args):
    program_times = {}

    do_chromatic = args.lowest_note != -1
    # ---------------------------------------------------------------------
    # Parse the midi file:
    start = timer()
    mid = mido.MidiFile(args.midi_file)
    ignore = []
    if args.track != -1:
        # print()
        ignore = [i for i in range(1,50) if i != args.track]
    print("ignore:",ignore)
    notes, tempo, total_ticks = merge_parse(mid, ignore) # else parseMidi(mid, args)
    end = timer()

    if args.print_track:
        print_notes(notes)
        exit(0)

    program_times['midi'] = end - start
    print("----------------------------\nMidi parsed in:", program_times['midi'], "s")

    #exit(0)





    # ---------------------------------------------------------------------
    # Initialize the video:
    start = timer()
    # rows = args.voices
    v = Video(args.clip, args.timestamps, rows=args.voices,cols=args.voices,text=do_chromatic,quality=args.quality,do_fade=True,only_audio=False)

    end = timer()
    program_times['initialize'] = end - start
    print("----------------------------\nVideo initialized in:", program_times['initialize'], "s")

    print(len(notes), "notes")


    #################### misirlou test:
    #notes = misirlou()

    #################### Chromatic test:
    # min 50
    if do_chromatic:
        notes = chromatic(lowest = args.lowest_note, highest = 76, duration = 1)
        # notes = chromatic(lowest = args.lowest_note, highest = args.lowest_note+12, duration = 1)


    #################### Octaves test:
    # min 50
    #notes = octaves(lowest = 50, highest = 96, duration = 0.5)

    # print(notes)
    # print('120 ticks = ', mido.tick2second(120, mid.ticks_per_beat, tempo))

    # ---------------------------------------------------------------------
    # Add notes to video (generate clips)
    start = timer()
    curr = 0 # ticks
    curr_s = 0 # secs
    full = mid.length

    msg_freq = 0.01
    next_msg = msg_freq

    desired_length = args.max_duration # sec
    for (note, vel, ticks) in notes:
        curr += ticks
        t = mido.tick2second(ticks, mid.ticks_per_beat, tempo) if not do_chromatic else ticks
        curr_s += t
        # just some feedback:
        # curr_s = mido.tick2second(curr, mid.ticks_per_beat, tempo)
        if curr_s >= next_msg*min(full, desired_length): # percentage advanced
            print("now at:", int(100*next_msg), "% processed: ", curr_s, "s")
            next_msg += msg_freq
        if curr_s >= desired_length:
            break
        if note == -1: # tempo change!!
            tempo = vel
            v.add_time(t)
        elif note == -2: # unknown msg, only add time
            v.add_time(t)
        elif curr_s>=args.initial_t: # normal notes
            v.addNote(note, vel, t) # this is the important stuff


    # tick_converted= mido.second2tick(full, mid.ticks_per_beat, tempo)
    # if tick_converted != full:
    #     print('1??', tick_converted,total_ticks)
    if curr != total_ticks:
        print('Warning: Wrong ticks!!', curr, '!=', total_ticks)
    if v.current_time != full:
        print('Warning: Wrong time!! (video != expected):', v.current_time, '!=', full)
        # exit(1)
    if curr_s != full:
        print('Warning: Wrong time!! (current != expected):', curr_s, '!=', full)
        # exit(1)

    end = timer()

    program_times['clips'] = end - start
    print("----------------------------\nClips generated in:", program_times['clips'], "s")
    print("Compiling... ", end="")

    # ---------------------------------------------------------------------
    # Merge clips and save:
    start = timer()
    v.compile(args.output)
    end = timer()
    program_times['join'] = end - start
    print("----------------------------\nVideo joined in:", program_times['join'], "s")
    total_t = sum(program_times.values())
    print('----------------------------\nTotal:', total_t, '\nTime in each step:')
    for name, t in program_times.items():
        print(name, '->', 100 * t / total_t, "%")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--midi_file', help='Midi file', type=str, default="bumble_bee.mid")
    # TODO: permitir usar todas las tracks!!
    parser.add_argument('-tr', '--track', help='Number of the track from the midi to generate (default: all)', type=int, default=-1)
    parser.add_argument('-c', '--clip', help='original video', type=str, default="original/escala.mp4")

    # parser.add_argument('-i2', '--input2', help='Input video file 2', type=str, default="")
    parser.add_argument('-t', '--timestamps', help='timestamps for each note in the video', type=str, default="original/times-escala.csv")
    parser.add_argument('-o', '--output', help='output file', type=str, default="out.mp4")


    parser.add_argument('-v', '--voices', help='output file', type=int, default=1)

    parser.add_argument('-s', '--slow', help='slow mo (-s 2 makes it twice as slow)', type=float, default=1)
    parser.add_argument('-ini', '--initial_t', help='initial time (s) in midi to start video', type=float, default=0)
    parser.add_argument('-max', '--max_duration', help='max output duration', type=float, default=100000)


    parser.add_argument('-q', '--quality', help='reduce quality (e.g. 0.5)', type=float, default=1)

    parser.add_argument('-low', '--lowest_note', help='make a chromatic scale starting at this note', type=int, default=-1)

    parser.add_argument('-pt', '--print_track', help='Print the notes from the track', dest='print_track', action='store_true')
    parser.set_defaults(print_track=False)



    args = parser.parse_args()
    main(args)

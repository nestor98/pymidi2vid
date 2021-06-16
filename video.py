
import math
from moviepy.editor import *


def getMinMax(d):
    """look away"""
    min = 10000000
    max = -1000000
    for k in d.keys():

        if k<min:
            min = k
        elif k>max:
            max = k
    return min, max



class Video(object):
    """docstring for Video."""


    def __init__(self, original, timestamps_file, rows=2, cols=2, quality=0.25, eps=0.2, infinite_subclips=False):
        """
        original: the original video file
        timestamps_file: the file with the start time for each note
        max_notes: unused for now
        voices: number of desired voices in the output
        eps (s) is a fix for very short notes
        """
        #self.ticks2sec = ticks2sec # function to convert midi ticks to seconds
        self.inf_subclips = infinite_subclips # not implemented yet
        self.original = VideoFileClip(original).resize(quality)
        ##self.original = self.original.resize(height=90) # reduce quality, more speed?
        self.end_size = self.original.size
        self.voices = rows*cols # number of channels
        self.original = self.original.resize(1.0/math.sqrt(self.voices))
        self.rows = rows #int(math.sqrt(self.voices))
        self.cols = cols #int(voices / self.rows)

        self.timestamps = {} # tiempo (s) de inicio de cada nota en el video
        self.notes = {} # clips
        self.loadTimeStamps(csv=timestamps_file)
        # for k in self.timestamps:
        #     print(k)
        self.lowest, self.highest = getMinMax(self.timestamps)
        print(self.lowest, self.highest)

        self.eps = eps

        self.memoized_count = 0
        ############################ TEMP
        # self.fillMissing(0, 127)
        # print("nota, t:")
        # for n, t in self.timestamps.items():
        #     print(n, t)
        ############################
        self.max_note_length = 10 # DE MOMENTO
        self.pending_notes = {}  # notes to be finished
        self.current_time = float(0) # current time in ticks (all notes before it are already clips)
        self.clips = [] # all clips for final video
        self.clips_at_time = {} # for each t, number of notes at that time
        self.subnotes = {} # {note : {duration: clip}} subclips of the notes, to cache shorter notes and speed up the process

    def loadTimeStamps(self, csv="times.csv", sep=';', other_seps=[' ', '\t']):
        with open(csv, 'r') as f:
            for line in f:
                for o in other_seps:
                    line = line.replace(o, sep)
                l = line.split(sep)
                if len(l) > 1:
                    self.timestamps[int(l[0])] = float(l[1])

    def add_time(self, t):
        self.current_time += t

    def fillMissing(self, min, max):
        """
        Fills the missing notes between min and max with the timestamp 0
        """
        for i in range(min, max):
            if i not in self.timestamps:
                self.timestamps[i] = float(0)

    def queueNote(self, note, vel):
        """ Adds a note at the current time with vel velocity """
        self.pending_notes[note] = (vel, self.current_time)

    def placeClip(self, clip, i):
        """ sets the clip position in one of the rows/cols according to i """
        i = i%self.voices # temp: just place new clips on top of older ones
        if i < self.voices:
            row = i // self.cols
            col = i % self.cols
            return clip.set_position((float(col)/float(self.cols), float(row)/float(self.rows)), relative=True)
        #else: # doesnt work
            #return clip.audio
    # def placeClip_inf(self, clip, i, depth):
    #     row = i // self.cols
    #     col = i % self.cols
    #     if not self.inf_subclips or row == 0 or col == 0:
    #         return clip.set_position((float(col)/float(self.cols), float(row)/float(self.rows)), relative=True)
    #     else:
    #         i -= 3
    #         subrow =


    def endNote(self, note):
        """ Ends the note, adding its clip to the clip list at the corresponding time and position """
        note_info = self.pending_notes[note] # velocity and time
        clip_ini = note_info[1] # time when the clip starts playing in the end vid
        note_length = self.current_time-clip_ini
        if note_length > 0: # if the duration is zero, return
            note_ini = self.timestamps[note]
            note_length = min(note_length, self.max_note_length)
            if note_length < self.eps: # if note is very short, add eps to start (to make sure it sounds)
                note_ini += self.eps
            if note not in self.subnotes: # memoizacion para no recomponer siempre los subclips
                self.subnotes[note] = {}
            if note_length not in self.subnotes[note]:
                self.subnotes[note][note_length] = self.original.subclip(note_ini, note_ini+note_length).fx(afx.audio_normalize) # clip of <note> of duration <b>
            else: # just for stats
                self.memoized_count += 1
            # Get the position in the grid:
            if clip_ini not in self.clips_at_time:
                self.clips_at_time[clip_ini] = 1
            else:
                self.clips_at_time[clip_ini] += 1 # number of clips at the same time
            n = self.clips_at_time[clip_ini]-1 # idx of position
            vel = float(note_info[0]) / 127.0 # velocity between 0 and 1 -> volume
            # Append the clip at the position, set its start time (in the end video) and its volume:
            self.clips += [self.placeClip(self.subnotes[note][note_length].set_start(clip_ini), int(n)).volumex(vel)]
        self.pending_notes[note] = None

    def clampToRange(self, note):
        """ Changes the octave of note to be in the available range. Shitty implementation """
        while note > self.highest:
            note -= 12
        while note < self.lowest:
            note += 12
        return note

    def addNote(self, note, vel, time):
        """
        Adds the note <note> (midi code) with <vel> velocity (volume) at <ticks> ticks
        If vel==0 it ends the note
        """
        self.current_time += time
        note = self.clampToRange(note)
        if vel != 0: # start of note
            self.queueNote(note, vel)
        else: # end of note
            if note in self.pending_notes and self.pending_notes[note] is not None:
                self.endNote(note)


    def compile(self, output):
        """ Generate the video from all the clips and save it to output (path) file """
        print("len: ", len(self.clips))
        print("reused:", self.memoized_count, "clips")
        result = CompositeVideoClip(self.clips, size=self.end_size)
        result.write_videofile(output,fps=25, threads=11)

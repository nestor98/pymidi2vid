# pymidi2vid

Play any song in video. Take a midi of the song, a video of yourself playing individual notes, and witness the magic.

## Teaser
[![Flight of the Bumblebee](http://img.youtube.com/vi/I3syTzmhDcQ/0.jpg)](http://www.youtube.com/watch?v=I3syTzmhDcQ "Flight of the Bumblebee is not that hard")

## Installation
- Make a [virtual environment](https://docs.python.org/3/library/venv.html) (```python3 -m venv .```, etc.).
- ```pip3 install -r requirements.txt```

## Usage
- Record yourself playing an instrument one note at a time, ascending a half step at a time, with silences in between.
- Use audiosegmentation.py to find where each note starts:
```
python3 audiosegmentation.py -i original/flea.mp4 -l 28 -s 0.3 -w 0.7
```
- Probably fix the resulting csv (original/flea.csv in this case). If you played ```n``` notes, it should have ```n``` rows with ```notecode;time(s)``` in each row (where ```notecode``` is the midi code of the note).
- Use editor.py to make the video: 
```
python3 editor.py -c original/flea.mp4 -t original/flea.csv -v 1 -o output/classicalthumpfull.mp4 -m midis/Wooten,_Victor_-_Classical_Thump.mid
```

All scripts can be called with ```-h``` to show the help.

## Wait but how
- [Mido](https://github.com/mido/mido): to parse the midi file and get the notes, times, etc.
- [MoviePy](https://github.com/Zulko/moviepy): to split the original video in clips for each note, and compose them together to follow the song.

And, experimentally (for now):
- [pyAudioAnalysis](https://github.com/tyiannak/pyAudioAnalysis): to automate the process of generating the csv with the timestamps for each note, which is _not fun_ to do by hand.

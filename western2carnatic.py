import sys
from music21 import *

# parse MusicXML file
stream = converter.parse(sys.argv[1], format='musicxml')

# get key
key = stream.analyze('key')
sa = note.Note(key.tonic)
sa.octave = 3
_sa = sa.transpose('P8') # higher S

# get range of notes (in ragam and overall)
raga_scale = key.getPitches(sa.nameWithOctave, _sa.nameWithOctave)
chromatic_scale = scale.ChromaticScale(sa.nameWithOctave).getPitches(
    sa.nameWithOctave, _sa.nameWithOctave)

# map western notes to Carnatic notes
carnatic_notes = dict(zip(
    [note.name for note in chromatic_scale],
    ['s', 'r1', 'r2/g1', 'r3/g2', 'g3', 'm1', 'm2', 
    'p', 'd1', 'd2/n1', 'd3/n2', 'n3']
))

carnatic_notes.update(dict(zip(
    [note.name for note in raga_scale],
    ['s', 'r', 'g', 'm', 'p', 'd', 'n']
)))

# traverse the score tree
for part in stream.recurse().parts:
    for note in part.recurse().notes:
        # ignore chords (for now)
        if note.isChord:
            note.lyric = '?'
            continue
  
        # replace lyric with Carnatic note
        if note.name in carnatic_notes:
            note.lyric = carnatic_notes[note.name]
            continue

        # if note is not in mapping, use lower enharmonic
        lower = note.pitch.getLowerEnharmonic().name
        if lower in carnatic_notes:
            note.lyric = carnatic_notes[lower]
            continue
        
        # if note still not in mapping, use higher eharmonic
        higher = note.pitch.getHigherEnharmonic().name
        if higher in carnatic_notes:
            note.lyric = carnatic_notes[higher]
            continue
        
        note.lyric = '?'

# show sheet music in Musescore
stream.show()
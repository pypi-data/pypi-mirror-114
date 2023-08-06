import mido
from .columns.midi_columns import *
import time

def byTimeUnitToMidi(df, smallestTimeUnit, tpb = 64):
    mf = mido.MidiFile(ticks_per_beat=tpb)
    track = mido.MidiTrack()
    mf.tracks.append(track)
    ticksPerTimeUnit = 4 * smallestTimeUnit * tpb
    dt = 0
    for noteOns, noteOffs in zip(df[CurrentNoteOnColumn.NAME], df[CurrentNoteOffColumn.NAME]):
        dt+=1
        if(len(noteOns)==0 and len(noteOffs)==0):
            dt+=1
            continue

        if(len(noteOns)>0):
            for noteOn in noteOns:
                if(dt>0):
                    track.append(mido.Message("note_on", note = int(noteOn), time = int(dt*ticksPerTimeUnit)))
                    dt = 0
                else:
                    track.append(mido.Message("note_on", note = int(noteOn), time = 0))

        if(len(noteOffs)>0):
            for noteOff in noteOffs:
                if(dt>0):
                    track.append(mido.Message("note_off", note = int(noteOff), time = int(dt*ticksPerTimeUnit)))
                    dt = 0
                else:
                    track.append(mido.Message("note_off", note = int(noteOff), time = 0))
    mf.save(str(time.time())+".mid")



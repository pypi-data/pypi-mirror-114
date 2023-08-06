import mido
from mido import MidiFile
from os import path,walk
import warnings
import os
from tqdm import tqdm
import pandas as pd
from pandas import DataFrame

"""Least common divisor. Used to used smallestTimeUnit in normalization"""
def lcd(lst):
    testingValue = min([element for element in lst if element != 0])
    while 1:
        nextLoop = False
        for value in lst:
            if(value%testingValue!=0):
                testingValue -= 1
                nextLoop = True
        if(nextLoop):
            continue
        return testingValue
    
        
def normalizeTicks(ticks, tpb, smallestTimeUnit):
    converted = ticks*(1/tpb)/4/smallestTimeUnit
    if(converted>0 and converted<1):
        warnings.warn(f"smallestTimeUnit {smallestTimeUnit} not small enough to capture {ticks} ticks under {tpb} ticks per beat.  \
                       This tick value is converted to {converted} ticks.")
        converted=1
    return round(converted)

def findMidis(folder, r=True):
    paths = []
    if(".mid" in folder):
        paths.append(folder)
        return paths

    for (dirpath, _, filenames) in walk(folder):
        for file in filenames:
            if ".mid" in file:
                paths.append(path.join(dirpath, file))
        if not r:
            return paths
    return paths



"""Abstracted class that preprocesses digital forms of music into dataframes"""
class PieceCompiler:
    """
    columns: Column
        Initialized Column instance
    validateFunction: function
        condition for events to be valid
    """
    def __init__(self, columns, validateFunction):
        self.columns = columns
        self.validateFunction = validateFunction
        self.pieces = self.getPieces()
        self.df = DataFrame(columns = [column.name for column in columns])

    def getPieces(self):
        raise NotImplementedError("Must implement getPieces function")

    def appendColumn(self, column):
        self.columns.append(column)

    def compile(self):
        for pieceID, piece in tqdm(enumerate(self.pieces)):
            pieceDfEvents = []
            for eventID, event in enumerate(piece):
                if(self.validateFunction(event)):
                    dfEvent = {}
                    dfEvent["pieceID"] = pieceID
                    for column in self.columns:
                        dfEvent[column.name] = column.eventFunction(event) if column.enum == False else column.eventFunction(eventID, piece)
                    pieceDfEvents.append(dfEvent)
            self.df = self.df.append(pieceDfEvents, ignore_index=True)
        return self.df
        


"""Midi version of the piece compiler"""
class MidiPC(PieceCompiler):
    def __init__(self, midiPaths, columns, validateFunction, *args, **kwargs):
        super().__init__(columns, validateFunction, *args, **kwargs)
        self.midiPaths = findMidis(midiPaths)
        

    def getPieces(self):
        for i in range(len(self.midiPaths)):
            mf = MidiFile(self.midiPaths[i])
            tpb = mf.ticks_per_beat
            mf = mido.merge_tracks(mf.tracks)
            mf.ticks_per_beat = tpb
            yield mf

    """Normalize any time column ticks to time units"""
    def normalizeTicks(self, tickColumnName, tpbColumnName = "tpb", smallestTimeUnit = 1/32):
        self.df[tickColumnName] = [normalizeTicks(ticks, tpb, smallestTimeUnit) for ticks, tpb in zip(self.df[tickColumnName], self.df[tpbColumnName])]

    """Records time in terms of duration. Rest = -1 for note column"""
    def convertDurational(self, typeColumnName = "type", noteColumnName = "note"):
        pass








import os
def testMidiPC():
    pass
    


if __name__ == "__main__":
    testMidiPC()
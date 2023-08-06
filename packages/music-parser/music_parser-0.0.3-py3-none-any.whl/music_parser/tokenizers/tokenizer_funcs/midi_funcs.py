from ...columns.midi_columns import *
import pandas as pd
from tqdm import tqdm

"""Functions that are used in midi_tokenizers"""


"""Mainly used just for MLB tokenizer"""
def splitByTimeUnit(df):
    newDf = pd.DataFrame(columns=[CurrentNoteOnColumn.NAME,CurrentNoteOffColumn.NAME])
    for eventID, dt in tqdm(enumerate(df[DTColumn.NAME])):
        if(eventID>0 and dt!=0):
            newDf = newDf.append({
                CurrentNoteOnColumn.NAME:df[CurrentNoteOnColumn.NAME][eventID-1],
                CurrentNoteOffColumn.NAME:df[CurrentNoteOffColumn.NAME][eventID-1],
                PieceID.NAME:df[PieceID.NAME][eventID-1]
            }, ignore_index=True)
            newDf = newDf.append([{CurrentNoteOnColumn.NAME:[], CurrentNoteOffColumn.NAME:[], PieceID.NAME:df[PieceID.NAME][eventID]} for i in range(dt-1)], ignore_index=True)
    return newDf



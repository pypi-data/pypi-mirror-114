from .tokenizer import *
from .tokenizer_funcs.midi_funcs import *
from ..columns.midi_columns import *
import pandas as pd
from functools import partial

"""Tokenizes different forms of midi dataframes"""






"""Dataframe must have -current_note_ons, -current_note_offs, -dt, -pieceID columns"""
class MLBTokenizer(Tokenizer):
    def __init__(self):
        fns = [
            partial(dropColumnsExcept, columnsToNotDrop = ["current_note_ons", "current_note_offs", "dt", "pieceID"]),
            splitByTimeUnit
        ]

        checks = [CurrentNoteOffColumn.NAME, CurrentNoteOnColumn.NAME, DTColumn.NAME, PieceID.NAME]

        super().__init__(fns, checks)





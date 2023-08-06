from .piece_compiler import *
from .columns.midi_columns import *


def midiOnOff(midiPaths):
    columns = [
        DTColumn(),
        TypeColumn(),
        NoteColumn(),
        TPBColumn()
    ]
    
    return MidiPC(midiPaths, columns, lambda x: x.type in ["note_on", "note_off"])

from .column import Column


class PieceID:
    NAME = "pieceID"


"""Used to quickly declare midi dt column"""
class DTColumn(Column):

    NAME = "dt"

    def __init__(self):
        super().__init__(DTColumn.NAME, eventFunction=lambda x: x.time, enum=False)

class TypeColumn(Column):

    NAME = "type"

    def __init__(self):
        super().__init__(TypeColumn.NAME, eventFunction=lambda x: x.type, enum=False)


class NoteColumn(Column):

    NAME = "note"

    def __init__(self):
        super().__init__(NoteColumn.NAME, eventFunction=lambda x: x.note, enum=False)



class TPBColumn(Column):

    NAME = "tpb"

    def __init__(self):
        super().__init__(TPBColumn.NAME, eventFunction=lambda eventID, piece: piece.ticks_per_beat, enum=True)



class CurrentNoteOnColumn(Column):

    NAME = "current_note_ons"

    def __init__(self):
        super().__init__(CurrentNoteOnColumn.NAME, eventFunction=CurrentNoteOnColumn.collectNoteOffs, enum=True)

    """For each time step records note ons"""
    @staticmethod
    def collectNoteOns(eventID, piece):
        note_ons = [] 
        while(eventID>=0 and piece[eventID].time == 0):
            if(piece[eventID].type == "note_on"):
                note_ons.append(piece[eventID].note)
            eventID -= 1
        if(eventID>=0 and piece[eventID].type == "note_on"):
            note_ons.append(piece[eventID].note)
        return note_ons
    



class CurrentNoteOffColumn(Column):

    NAME = "current_note_offs"

    def __init__(self):
        super().__init__(CurrentNoteOffColumn.NAME, eventFunction=CurrentNoteOffColumn.collectNoteOffs, enum=True)

    """For each time step records note offs"""
    @staticmethod
    def collectNoteOffs(eventID, piece):
        note_ons = [] 
        while(eventID>=0 and piece[eventID].time == 0):
            if(piece[eventID].type == "note_off"):
                note_ons.append(piece[eventID].note)
            eventID -= 1
        if(eventID>=0 and piece[eventID].type == "note_off"):
            note_ons.append(piece[eventID].note)
        return note_ons

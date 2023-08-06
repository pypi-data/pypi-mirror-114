class Column:
    """
    name: str
        Name that will be used on dataframe
    eventFunction: function
        Function that returns aspect of event to record in df column
    enum: bool
        Whether the event function should have access to entire piece
    """
    def __init__(self, name, eventFunction, enum = False):
        self.name = name
        self.eventFunction = eventFunction
        self.enum = enum
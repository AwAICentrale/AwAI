class NotInYourSideError(Exception):
    def __init__(self):
        self.message = "You tried to play a pit that's not your side of the board !"

    def __str__(self):
        return self.message


class EmptyPitError(Exception):
    def __init__(self):
        self.message = "You tried to play an empty pit"

    def __str__(self):
        return self.message


class StarvationError(Exception):
    def __init__(self):
        self.message = "You mustn't starve your opponent"

    def __str__(self):
        return self.message

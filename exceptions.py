class NotInYourSideError(Exception):
    def __init__(self):
        self.message = "You try to play a pit that's not your side of the board !"
    def __repr__(self):
        print(self.message)   

class EmptyPitError(Exception):
    def __init__(self):
        self.message = "You try to play a emplty pit"
    def __repr__(self):
        print(self.message)

class StarvationError(Exception):
    def __init__(self):
        self.message = "You mustn't starve your opponent"
    def __repr__(self):
        print(self.message)
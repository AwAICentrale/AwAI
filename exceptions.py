class NotInYourSideError(Exception):
    def __init__(self):
        self.message = "You try to play a pit that's not your side pf the board !"
    def __str__(self):
        print(self.message)   

class EmptyPitError(Exception):
    def __init__(self):
        self.message = "You try to play a emplty pit"
    def __str__(self):
        print(self.message)

class StarvationError(Exception):
    def __init__(self):
        self.message = "You mustn't starve your opponent"
    def __str__(self):
        print(self.message)
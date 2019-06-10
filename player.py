class Player:
    """docstring for Player."""
    def __init__(self, typePlayer):
        self.typePlayer = typePlayer
        if self.typePlayer == "random":
            self.player = Random()
        elif self.typePlayer == "minimax":
            self.player = Minimax(None,None,None)
        elif self.typePlayer == "minimaxAB":
            self.player = MinimaxAlphaBeta(None,None,None)



    def play(self):
        self.player.play()
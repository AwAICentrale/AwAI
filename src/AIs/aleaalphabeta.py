from src.AIs.alea import Alea


class AleaAlphaBeta(Alea):
    def __init__(self, game, stage):
        super().__init__(game)
        self.stage = stage

    def play(self):
        if self.stop_playing(self.stage) == "STOP":
            return "STOP"
        return super().play()

    def stop_playing(self, stage):
        nb_seeds_begin = 5
        nb_seeds_midgame = 19
        if stage == "begin":
            if (self.game.player0.loft >= nb_seeds_begin) or \
                    (self.game.player1.loft >= nb_seeds_begin):
                return "STOP"
        if stage == "midgame":
            if (self.game.player0.loft >= nb_seeds_midgame) or \
                    (self.game.player1.loft >= nb_seeds_midgame):
                return "STOP"

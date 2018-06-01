import time


class GameState(object):
    def __init__(self):
        self._start_time = time.time()

    @property
    def time_elapsed(self):
        return time.time() - self._start_time


class Idle(GameState):
    pass

class WaitingForInput(GameState):
    pass

class PlayingSequence(GameState):
    pass

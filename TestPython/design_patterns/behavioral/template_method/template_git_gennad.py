

class AbstractGame:
    """An abstract class that is common to several games in which
    players play against the others, but only one is playing at a
    given time.
    """
    def __init__(self, *args, **kwargs):
        if self.__class__ is AbstractGame:
            raise TypeError('abstract class cannot be instantiated')

    def play_one_game(self, players_count):
        self.players_count = players_count
        self.initialize_game()
        j = 0
        while not self.end_of_game():
            self.make_play(j)
            j = (j + 1) % self.players_count
        self.print_winner()

    def initialize_game(self):
        raise TypeError('abstract method must be overridden')

    def end_of_game(self):
        raise TypeError('abstract method must be overridden')

    def make_play(self, player_num):
        raise TypeError('abstract method must be overridden')

    def print_winner(self):
        raise TypeError('abstract method must be overridden')


# Now to create concrete (non-abstract) games, you subclass AbstractGame
# and override the abstract methods.

class Chess(AbstractGame):
    def initialize_game(self):
        # Put the pieces on the board.
        pass

    def make_play(self, player):
        # Process a turn for the player
        pass

# --------- Alex's Martelli example ---------


class AbstractBase(object):
    def orgMethod(self):
        self.doThis()
        self.doThat()


class Concrete(AbstractBase):

    def doThis(self):
        pass

    def doThat(self):
        pass

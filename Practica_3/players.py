from minimax import minimax_search
from alphabeta import alphabeta_search
import random

def abstract():
    import inspect
    caller = inspect.getouterframes(inspect.currentframe())[1][3]
    raise NotImplementedError(caller + ' must be implemented in subclass')



class Player:
    """
    Generic player for an adversarial game. Subclasses must implement the
    get_next_action method
    """
    
    def get_next_action(self, game_state):
        abstract()
    
#-------------------------------------------------------------
# Player definitions

class RandomPlayer(Player):
    """
    Random player for an adversarial game. It plays a random action chosen
    among the possible ones
    """
    
    def get_next_action(self, game_state):
        actions = game_state.possible_actions()
        return random.choice(actions)


class MinimaxPlayer(Player):
    """
    A more 'intelligent' player, choosing an action by means of the 
    minimax algorithm     
    """
    
    def __init__(self, max_depth):
        self.max_depth = max_depth
        
    def get_next_action(self, game_state):
        return minimax_search(game_state, self.max_depth)


class AlphabetaPlayer(Player):
    """
    A more 'intelligent' player, choosing an action by means of the 
    alpha-beta pruning version of the minimax algorithm     
    """
    
    def __init__(self, max_depth, eval_fn):
        self.max_depth = max_depth
        self.eval_fn = eval_fn
        
    def get_next_action(self, game_state):
        return alphabeta_search(game_state, self.max_depth, self.eval_fn)
    

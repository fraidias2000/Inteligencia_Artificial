
# AlphaBeta Partial Search

infinity = 1.0e400


def terminal_test(state, depth):
    return depth <= 0 or state.is_terminal

def max_value(state, player, max_depth, alpha, beta, eval_function):
    if max_depth >0:
        if terminal_test(state,max_depth):
         return eval_function(state,player)
        v=-infinity
        for a in state.possible_actions():
         v=max(v,min_value(state.result_state(a),player, max_depth-1,alpha,beta,eval_function))
         if v>=beta:
             return v
         alpha=max(alpha,v)
        return v

    
    """
    Completar con el codigo correspondiente a la funcion <max_value> de la
    version del algoritmo minimax con poda alfa-beta
    """

def min_value(state, player, max_depth, alpha, beta, eval_function):
    if max_depth >0:
        if terminal_test(state,max_depth):
         return eval_function(state,player)
        v=infinity
        for a in state.possible_actions():
         v=min(v,max_value(state.result_state(a),player, max_depth-1,alpha,beta,eval_function))
         if v<=alpha:
             return v
         beta=min(beta,v)
        return v

    """
    Completar con el codigo correspondiente a la funcion <min_value> de la
    version del algoritmo minimax con poda alfa-beta
    """


def alphabeta_search(game, max_depth, eval_function):
    """
    Search game to determine best action; use alpha-beta pruning.
    This version cuts off search and uses an evaluation function.
    """

    player = game.current_player

    # Searches for the action leading to the sucessor state with the highest min score
    successors = game.successors()
    best_score, best_action = -infinity, successors[0][0]
    for (action, state) in successors:
        score = min_value(state, player, max_depth, -infinity, infinity, eval_function)
        if score > best_score:
            best_score, best_action = score, action
    
    return best_action

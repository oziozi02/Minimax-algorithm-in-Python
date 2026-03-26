import random
import time
import n_tree
from state import State
from n_tree import NTreeNode
from minimax_tree import MiniMaxTree

class Agent:
    ident = 0

    def __init__(self):
        self.id = Agent.ident
        Agent.ident += 1

    def get_chosen_action(self, state, max_depth):
        pass


class RandomAgent(Agent):
    def get_chosen_action(self, state, max_depth):
        time.sleep(0.5)
        actions = state.get_legal_actions()
        return actions[random.randint(0, len(actions) - 1)]


class GreedyAgent(Agent):
    def get_chosen_action(self, state, max_depth):
        time.sleep(0.5)
        actions = state.get_legal_actions()
        best_score, best_action = None, None
        for action in actions:
            new_state = state.generate_successor_state(action)
            score = new_state.get_score(state.get_on_move_chr())
            if (best_score is None and best_action is None) or score > best_score:
                best_action = action
                best_score = score
        return best_action
    

def visit_node_n(node: NTreeNode, state: State, depth: int, max_depth: int, turn: int) -> None:
        if depth == max_depth or not state.get_legal_actions():
            scores_dict = state.get_scores()
            values = [0] * state.get_num_of_players()
            for player_index in range(state.get_num_of_players()):
                player_letter = chr(ord('A') + player_index)
                values[player_index] = scores_dict[player_letter]
            node.set_values(values)
            return

        actions = state.get_legal_actions()
        for action in actions:
            child_node = NTreeNode(node, state.get_num_of_players(), action)
            node.add_child(child_node)

        new_turn = (turn + 1) % state.get_num_of_players()

        for child in node.children:
            new_state = state.generate_successor_state(child.action)
            visit_node_n(child, new_state, depth + 1, max_depth, new_turn)
        
        best_values = [float('-inf')] * state.get_num_of_players()
        for child in node.children:
            child_values = child.values
            if child_values[turn] > best_values[turn]:
                best_values = child_values.copy()

        node.set_values(best_values)
    
class MaxNAgent(Agent):
    def get_chosen_action(self, state, max_depth):
        time.sleep(0.5)
        actualState: State = state
        root: NTreeNode = NTreeNode(None, state.get_num_of_players(), None)
        current_player = actualState.get_on_move_ord()
        rounds_left = (actualState.get_max_rounds() - actualState.get_current_round() + 1) * actualState.get_num_of_players()
        rounds_left -= current_player
        depth = min(max_depth, rounds_left)
        visit_node_n(root, actualState, 0, depth, current_player)
        best_action = None
        best_value = float('-inf')
        for child in root.children:
            if child.values[current_player] > best_value:
                best_value = child.values[current_player]
                best_action = child.action

        return best_action


def visit_node_minimax(node: MiniMaxTree, state: State, depth: int, max_depth: int, is_maximizing_player: bool, current_player: str) -> None:
        if depth == max_depth or not state.get_legal_actions():
            scores = state.get_scores()
            if current_player == 'A':
                score = scores['A'] - scores['B']
            else:
                score = scores['B'] - scores['A']
            node.set_value(score)
            return

        actions = state.get_legal_actions()
        for action in actions:
            child_node = MiniMaxTree(action=action)
            node.add_child(child_node)

        for child in node.children:
            new_state = state.generate_successor_state(child.action)
            visit_node_minimax(child, new_state, depth + 1, max_depth, not is_maximizing_player, current_player)

        if is_maximizing_player:
            node.set_value(max(child.value for child in node.children))
        else:
            node.set_value(min(child.value for child in node.children))

class MiniMaxAgent(Agent):
    def get_chosen_action(self, state, max_depth):
        time.sleep(0.5)
        actualState: State = state
        root: MiniMaxTree = MiniMaxTree()
        current_player = actualState.get_on_move_chr()
        rounds_left = (actualState.get_max_rounds() - actualState.get_current_round() + 1) * 2
        if current_player == 'B':
            rounds_left -= 1
        depth = min(max_depth, rounds_left)
        visit_node_minimax(root, actualState, 0, depth, True, current_player)
        best_action = None
        best_value = float('-inf')
        for child in root.children:
            if child.value > best_value:
                best_value = child.value
                best_action = child.action

        return best_action
    

def visit_node_minimax_ab(node: MiniMaxTree, state: State, depth: int, max_depth: int, is_maximizing_player: bool, current_player: str, alpha: float, beta: float) -> None:
        if depth == max_depth or not state.get_legal_actions():
            scores = state.get_scores()
            if current_player == 'A':
                score = scores['A'] - scores['B']
            else:
                score = scores['B'] - scores['A']
            node.set_value(score)
            return

        actions = state.get_legal_actions()
        for action in actions:
            child_node = MiniMaxTree(action=action)
            node.add_child(child_node)

        if is_maximizing_player:
            value = float('-inf')
            for child in node.children:
                new_state = state.generate_successor_state(child.action)
                visit_node_minimax_ab(child, new_state, depth + 1, max_depth, False, current_player, alpha, beta)
                value = max(value, child.value)
                alpha = max(alpha, value)
                if beta <= alpha:
                    break
            node.set_value(value)
        else:
            value = float('inf')
            for child in node.children:
                new_state = state.generate_successor_state(child.action)
                visit_node_minimax_ab(child, new_state, depth + 1, max_depth, True, current_player, alpha, beta)
                value = min(value, child.value)
                beta = min(beta, value)
                if beta <= alpha:
                    break
            node.set_value(value)
    
class MiniMaxABAgent(Agent):
    def get_chosen_action(self, state, max_depth):
        time.sleep(0.5)
        actualState: State = state
        root: MiniMaxTree = MiniMaxTree()
        current_player = actualState.get_on_move_chr()
        rounds_left = (actualState.get_max_rounds() - actualState.get_current_round() + 1) * 2
        if current_player == 'B':
            rounds_left -= 1
        depth = min(max_depth, rounds_left)
        alpha = float('-inf')
        beta = float('inf')
        visit_node_minimax_ab(root, actualState, 0, depth, True, current_player, alpha, beta)
        best_action = None
        best_value = float('-inf')
        for child in root.children:
            if child.value > best_value:
                best_value = child.value
                best_action = child.action

        return best_action
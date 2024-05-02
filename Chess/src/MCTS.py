import random
import math
import copy

class MCTSNode:
    def __init__(self, board, move=None, parent=None):
        self.board = board
        self.move = move
        self.parent = parent
        self.children = []
        self.wins = 0
        self.visits = 0
        self.untried_moves = board.get_all_valid_moves()
        self.player_just_moved = 'black' if board.next_player == 'white' else 'white'
    
    def UCTSelectChild(self):
        """Select a child node with highest UCT value."""
        c = math.sqrt(2)
        return max(self.children, key=lambda child: child.wins / child.visits + c * math.sqrt(math.log(self.visits) / child.visits))
    
    def AddChild(self, m, b):
        """Remove the move from untried_moves and add a new child node for this move."""
        child = MCTSNode(copy.deepcopy(b), move=m, parent=self)
        self.untried_moves.remove(m)
        self.children.append(child)
        return child

    def Update(self, result):
        """Update this node - one additional visit and an update of the win count."""
        self.visits += 1
        self.wins += result

def MCTS(rootstate, itermax, player_color):
    rootnode = MCTSNode(copy.deepcopy(rootstate))

    for i in range(itermax):
        node = rootnode
        state = copy.deepcopy(rootstate)

        # Selection
        while node.untried_moves == [] and node.children != []:
            node = node.UCTSelectChild()
            state.move_piece(node.move)

        # Expansion
        if node.untried_moves != []:
            m = random.choice(node.untried_moves) 
            state.move_piece(m)
            node = node.AddChild(m, state)  # Add child and descend tree

        # Simulation
        while state.get_all_valid_moves() != []:
            state.move_piece(random.choice(state.get_all_valid_moves()))

        # Backpropagation
        while node != None:
            node.Update(1 if node.player_just_moved == player_color else 0)
            node = node.parent

    return sorted(rootnode.children, key=lambda c: c.wins / c.visits)[-1].move

def run_mcts(board, player_color, itermax):
    root = MCTSNode(board)
    for _ in range(itermax):
        node = root
        state = copy.deepcopy(board)

        # Selection
        while node.untried_moves == [] and node.children != []:
            node = node.UCTSelectChild()
            state.move(node.move)

        # Expansion
        if node.untried_moves:
            m = random.choice(node.untried_moves)
            state.move(m)
            node = node.AddChild(m, state)

        # Simulation
        while not state.is_game_over():
            state.move(random.choice(state.get_all_valid_moves()))

        # Backpropagation
        while node:
            node.Update(1 if state.get_winner() == node.player_just_moved else 0)
            node = node.parent

    return max(root.children, key=lambda c: c.visits).move

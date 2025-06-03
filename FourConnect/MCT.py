import numpy as np
import random, pickle
import copy
import math
import ConnectFour
from Agent import Agent

class MCT_Nodes():
    def __init__(self, board : ConnectFour.ConnectFour, player, num_agents, team_member, col=None, parent=None):
        self.parent = parent
        self.children = []
        self.board = board
        self.N = 1
        self.Q = 0
        self.player = player
        self.num_agents = num_agents
        self.team_member = team_member
        self.col = col
    
    def selection(self):
        node = self
        while node.children != []:
            node = uct(node)

        return node

    def expansion(self):
        if self.board.is_game_over():
            return self
        legal_moves = self.board.get_legal_action()
        # if child not in children
        for col in legal_moves:
            new_board = copy.deepcopy(self.board)
            new_board.drop_piece(self.player, col)
            child = MCT_Nodes(new_board, (self.player+1)%self.num_agents, self.num_agents, self.team_member, col, self)
            if new_board.game_over:
                self.children = [child]
                break
        
            self.children.append(child)
        
        return random.choice(self.children)
    
        
    def simulation(self, iterations):
        winning_sum = 0
        for _ in range(iterations):
            player = self.parent.player
            board = copy.deepcopy(self.board)
            stuck = False
            while not board.is_game_over():
                player = (player+1)%self.num_agents
                cols = board.get_legal_action()
                move = None
                for col in cols:
                    row = board.get_top_row(col)
                    if board.check_potential_win(row, col, player):
                        move = col
                        break
                    next_player = (player+1)%self.num_agents
                    if next_player not in self.team_member:
                        if board.check_potential_win(row, col, next_player):
                            move = col
                            break
                        if board.check_potential_win(row-1, col, next_player):
                            cols.remove(col) 
                if cols == []:
                    stuck = True
                    break
                if move == None:
                    move = random.choice(cols)
            
                board.drop_piece(player, move)
            
            if stuck and player not in self.team_member:
                winning_sum += 1

            if board.game_over:
                if player in self.team_member:
                    winning_sum += 1
            else:
                winning_sum += 0.5

        return winning_sum

    def backpropagation(self, winning, iterations):
        node = self
        while node:
            node.N += iterations
            node.Q += winning
            node = node.parent
    

# uct algorithm
def uct(node : MCT_Nodes):
    best_score = float('-inf')
    best_node = None
    # loop all node in the children
    for child_node in node.children:
        # compute the ucb value
        
        ucb1_v1 = child_node.Q / child_node.N 
        ucb1_v2 = math.sqrt(2 * math.log(node.N) / child_node.N)
        score = ucb1_v1 + ucb1_v2
        if score > best_score:
            best_score = score
            best_node = child_node
    return best_node


class MCT_Agent(Agent):
    def __init__(self, id, team_sequence, iterations=100):
        super().__init__(id, team_sequence)
        
        self.iteration = iterations
        
    def make_move(self, game : ConnectFour, events = None):

        self.root = MCT_Nodes(game, self.id, self.agentCnt, self.team_member)
        
        # simulation
        for _ in range(self.iteration):
            node = self.root.selection()
            expanded_node = node.expansion()
            iter = 1
            
            winning_sum = expanded_node.simulation(iter)
            expanded_node.backpropagation(winning_sum, iter)

        
        best_child = max(self.root.children, key=lambda child: child.Q / child.N)
        return best_child.col

    def __str__(self):
        return "MCT Agent"
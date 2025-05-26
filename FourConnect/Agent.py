from ConnectFour import ConnectFour
import random
import copy
import pygame
from settings import *

class Agent:
    def __init__(self, id, team_sequence):
        self.id = id
        self.team_sequence = team_sequence
        self.team_member = [i for i in range(len(team_sequence)) if team_sequence[i] == self.id]

    def make_move(self, game: ConnectFour, events=None):
        pass

class HumanAgent(Agent):
    def make_move(self, game, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                col = event.pos[0] // CELL_SIZE
                return col
    
    def __str__ (self):
        return "Player"


class RandomAgent(Agent):
    def make_move(self, game: ConnectFour, events=None):
        valid_moves = [col for col in range(game.cols) if game.is_valid_location(col)]
        if valid_moves:
            return random.choice(valid_moves)
        return None

    def __str__ (self):
        return "Random Agent"

def naive_greedy_reward(game : ConnectFour, row, col, team_member):
    if game.is_game_over():
        return 100
    piece = game.get_chess(row, col)
    score = 0
    



class GreedyAgent(Agent):
    def __init__(self, reward_func = None):
        self.reward_func = reward_func

    def make_move(self, game : ConnectFour):
        valid_moves = [col for col in range(game.cols) if game.is_valid_location(col)]
        max_score = float('-inf')
        max_move = 0
        for move in valid_moves:
            temp_game = copy.deepcopy(game)
            _, row, col = temp_game.drop_piece(move)
            score = self.reward_func(temp_game, row, col, self.team_member)
            if score > max_score:
                max_score = score
                max_move = move
        return max_move

    def __str__ (self):
        return "Greedy Agent"
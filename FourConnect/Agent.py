from ConnectFour import ConnectFour
import random
import copy
import pygame
from settings import *

class Agent:
    def __init__(self, id, team_sequence):
        self.id = id
        self.team_sequence = team_sequence
        self.team_member = [i for i in range(len(team_sequence)) if team_sequence[i] == team_sequence[self.id]]
        self.agentCnt = len(self.team_sequence)

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
    score = 0
    
    def check_continuous(search_range):
        curChess = -1
        score = 0
        continuous_cnt = 0
        for r, c in search_range:
            if r < 0 or c < 0 or r >= game.rows or c >= game.cols:
                continue
            piece = game.get_chess(r, c)
            if piece == -1:
                continue
            if piece == curChess:
                continuous_cnt += 1
            else:
                if continuous_cnt == 2:
                    score += 5
                elif continuous_cnt == 3:
                    score += 10
                if piece not in team_member:
                    curChess = piece
                    continuous_cnt = 1
                else:
                    curChess = -1
                    continuous_cnt = 0

        if continuous_cnt == 2:
            score += 5
        elif continuous_cnt == 3:
            score += 10
        return score
    
    score += check_continuous([(row, col+i) for i in range(-3, 4)])
    score += check_continuous([(row+i, col) for i in range(1, 4)])
    score += check_continuous([(row+i, col+i) for i in range(-3, 4)])
    score += check_continuous([(row+i, col-i) for i in range(-3, 4)])
    
    return score

class GreedyAgent(Agent):
    def __init__(self, id, team_sequence, reward_func = None):
        super().__init__(id, team_sequence)
        self.reward_func = reward_func

    def make_move(self, game : ConnectFour, events):
        valid_moves = game.get_legal_action()
        max_score = float('-inf')
        max_move = 0
        for move in valid_moves:
            next_state, row = game.get_next_state(move, self.id)
            score = self.reward_func(next_state, row, move, self.team_member)
            if score > max_score:
                max_score = score
                max_move = move
        return max_move

    def __str__ (self):
        return "Greedy Agent"



def evaluate_func(game: ConnectFour, team_member, agentIndex):
    if game.game_over:
        if agentIndex in team_member:
            return 10
        else:
            return -10
    score = 0
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for row in range(game.rows):
        for col in range(game.cols):
            piece = game.get_chess(row, col)
            if piece == -1:
                continue
            for dr, dc in directions:
                count = 0
                for i in range(1, 4):
                    r, c = row + dr * i, col + dc * i
                    if 0 <= r < game.rows and 0 <= c < game.cols:
                        next_piece = game.get_chess(r, c)
                        if next_piece == piece:
                            count += 1
                        elif next_piece != -1:
                            break
                    else:
                        break
                if piece in team_member:
                    score += count
                else:
                    score -= count
    return score


class MiniMax(Agent):
    def __init__(self, id, team_sequence, depth, evaluate_func):
        super().__init__(id, team_sequence)
        self.depth = depth
        self.eval_func = evaluate_func


    def make_move(self, game : ConnectFour, events):
        alpha, beta = float('-inf'), float('inf')
        for action in game.get_legal_action():
            nextSate, row = game.get_next_state(action, self.id)
            v = self.next_value(nextSate, 0, self.id, alpha, beta)
            if v > alpha:
                alpha = v
                act = action
        return act
    
    def next_value(self, gameState : ConnectFour, depth, agentIndex, alpha, beta):
        nextIndex = (agentIndex + 1) % self.agentCnt
        if nextIndex == 0:
            depth += 1
        if gameState.is_game_over() or depth == self.depth:
            return self.eval_func(gameState, self.team_member, agentIndex)
        if nextIndex in self.team_member:
            return self.max_value(gameState, depth, nextIndex, alpha, beta)
        else:
            return self.min_value(gameState, depth, nextIndex, alpha, beta)
    
    def min_value(self, gameState : ConnectFour, depth, agentIndex, alpha, beta):
        v = float('inf')
        for action in gameState.get_legal_action():
            nextSate, row = gameState.get_next_state(action, agentIndex)
            v = min(v, self.next_value(nextSate, depth, agentIndex, alpha, beta))
            if v < alpha:
                return v
            beta = min(beta, v)
        return v
    
    def max_value(self, gameState : ConnectFour, depth, agentIndex, alpha, beta):
        v = float('-inf')
        for action in gameState.get_legal_action():
            nextSate, row = gameState.get_next_state(action, agentIndex)
            v = max(v, self.next_value(nextSate, depth, agentIndex, alpha, beta))
            if v > beta:
                return v
            alpha = max(alpha, v)
        return v


    def __str__(self):
        return "MiniMax Agent"
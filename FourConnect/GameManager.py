from settings import *
from ConnectFour import *
from Agent import *
import pygame


class GameManager:
    def __init__(self, agents : list[Agent], team_sequence = [0, 1], rows = 6, cols = 7):
        self.game = ConnectFour(rows=rows, cols=cols)
        self.agents = agents
        self.num_agents = len(agents)

        for i in range(self.num_agents):
            agents[i].set_agent_info(i, team_sequence)
        self.current_agent = 0

        self.window_size = (cols * CELL_SIZE, (rows + 1) * CELL_SIZE)
        self.screen = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption("Connect Four!!")
        self.draw_board()
    
    def draw_board(self):
        for row in range(self.game.rows):
            for col in range(self.game.cols):
                pygame.draw.rect(self.screen, (255, 255, 255), (col * CELL_SIZE, (row + 1) * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                pygame.draw.circle(self.screen, (0, 0, 0), (col * CELL_SIZE + CELL_SIZE // 2, (row + 1) * CELL_SIZE + CELL_SIZE // 2), RADIUS)
        pygame.display.flip()

    def update_board(self, row, col):
        player = int(self.game.get_chess(row, col))
        if player == -1:
            return
        color = COLORS[player]
        pygame.draw.circle(self.screen, color, (col * CELL_SIZE + CELL_SIZE // 2, (row + 1) * CELL_SIZE + CELL_SIZE // 2), RADIUS)
        pygame.display.flip()

    
    def update(self, events):
        
        row, col = None, None
        agent = self.agents[self.current_agent]
        if isinstance(agent, HumanAgent):
            col = agent.make_move(self.game, events)
        else:
            col = agent.make_move(self.game) 

        if col is not None:
            row = self.game.drop_piece(self.current_agent, col)    

        if row is not None:     
            self.update_board(row, col)
            self.current_agent = (self.current_agent + 1) % self.num_agents
            if self.game.is_game_over():
                if self.game.is_tie():
                    print("It's a draw!")
                else:
                    print(str(agent) + str(self.current_agent) + "wins!")
                return False
        return True
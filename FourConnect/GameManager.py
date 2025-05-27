from settings import *
from ConnectFour import *
from Agent import *
import pygame
import sys

pygame.init()

class GameState:
    MENU = 0
    PLAYING = 1
    GAME_OVER = 2

class GameManager:
    def __init__(self):
        self.width = 7* CELL_SIZE
        self.height = 6* CELL_SIZE
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("ConnectFour")
        
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 48)
        
        self.state = GameState.MENU
        self.game = ConnectFour()
        self.current_player = 0
        
        # meau button
        self.menu_buttons = [
            {"text": "Human VS Human", "rect": pygame.Rect(250, 160, 200, 50), "agents": [HumanAgent(0, [0,1]), HumanAgent(1, [0,1])]},
            {"text": "Human VS Radom", "rect": pygame.Rect(250, 220, 200, 50), "agents": [HumanAgent(0, [0,1]), RandomAgent(1, [0,1])]},
            {"text": "Human vs MiniMax", "rect": pygame.Rect(250, 280, 200, 50), "agents": [HumanAgent(0, [0,1]), MiniMax(1, [0,1], 4, evaluate_func)]},
            {"text": "Human vs Greedy", "rect": pygame.Rect(250, 340, 200, 50), "agents": [HumanAgent(0, [0,1]), GreedyAgent(1, [0, 1], naive_greedy_reward)]},
            {"text": "Human vs Qlearning", "rect": pygame.Rect(250, 400, 200, 50), "agents": [HumanAgent(0, [0,1]), QLearningAgent(1, [0,1])]},
            {"text": "Exit", "rect": pygame.Rect(250, 460, 200, 50), "agents": None}
        ]
        
        self.back_button = {"text": "Back", "rect": pygame.Rect(550, 10, 120, 40)}
        self.reset_button = {"text": "Restart", "rect": pygame.Rect(550, 60, 120, 40)}

    def draw_menu(self):
        self.screen.fill(COLORS[3])
        
        # title
        title = self.big_font.render("ConnectFour", True, COLORS[4])
        title_rect = title.get_rect(center=(self.width // 2, 100))
        self.screen.blit(title, title_rect)
        
        #draw button
        mouse_pos = pygame.mouse.get_pos()
        for button in self.menu_buttons:
            color = COLORS[6] if button["rect"].collidepoint(mouse_pos) else COLORS[5]
            pygame.draw.rect(self.screen, color, button["rect"])
            pygame.draw.rect(self.screen, COLORS[4], button["rect"], 2)
            
            text = self.font.render(button["text"], True, COLORS[4])
            text_rect = text.get_rect(center=button["rect"].center)
            self.screen.blit(text, text_rect)

    def draw_game(self):
        self.screen.fill((255, 255, 255))
        
        # draw map
        for row in range(self.game.rows):
            for col in range(self.game.cols):
                pygame.draw.rect(self.screen, COLORS[3], 
                               (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                pygame.draw.circle(self.screen, (255, 255, 255),
                                 (col * CELL_SIZE + CELL_SIZE // 2, 
                                  row * CELL_SIZE + CELL_SIZE // 2), RADIUS)
                
                # draw chess
                piece = self.game.get_chess(row, col)
                if piece != -1:
                    pygame.draw.circle(self.screen, COLORS[piece],
                                     (col * CELL_SIZE + CELL_SIZE // 2,
                                      row * CELL_SIZE + CELL_SIZE // 2), RADIUS)
        
        mouse_pos = pygame.mouse.get_pos()
        
        # BACK TO
        color = COLORS[6] if self.back_button["rect"].collidepoint(mouse_pos) else COLORS[5]
        pygame.draw.rect(self.screen, color, self.back_button["rect"])
        pygame.draw.rect(self.screen, COLORS[4], self.back_button["rect"], 2)
        text = self.font.render(self.back_button["text"], True, COLORS[4])
        text_rect = text.get_rect(center=self.back_button["rect"].center)
        self.screen.blit(text, text_rect)
        
        # RESTART
        color = COLORS[6] if self.reset_button["rect"].collidepoint(mouse_pos) else COLORS[5]
        pygame.draw.rect(self.screen, color, self.reset_button["rect"])
        pygame.draw.rect(self.screen, COLORS[4], self.reset_button["rect"], 2)
        text = self.font.render(self.reset_button["text"], True, COLORS[4])
        text_rect = text.get_rect(center=self.reset_button["rect"].center)
        self.screen.blit(text, text_rect)
        
        if not self.game.is_game_over():
            player_info = ""
            text = self.font.render(player_info, True, (0, 0, 0))
            self.screen.blit(text, (10, 10))
        else:
            if self.game.is_tie():
                result_text = "DRAW!"
            else:
                winner = self.agents[self.current_player].__str__()
                result_text = f"Player{self.current_player} {winner} WIN!"
            text = self.big_font.render(result_text, True, (255, 255, 255))
            text_rect = text.get_rect(center=(350, 550))
            self.screen.blit(text, text_rect)

    def handle_menu_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.menu_buttons:
                    if button["rect"].collidepoint(event.pos):
                        if button["agents"] is None:
                            pygame.quit()
                            sys.exit()
                        else:
                            self.agents = button["agents"]
                            self.game.reset_game()
                            self.current_player = 0
                            self.state = GameState.PLAYING

    def handle_game_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.back_button["rect"].collidepoint(event.pos):
                    self.state = GameState.MENU
                    return
                elif self.reset_button["rect"].collidepoint(event.pos):
                    self.game.reset_game()
                    self.current_player = 0
                    return
        
        if not self.game.is_game_over():
            current_agent = self.agents[self.current_player]
            col = current_agent.make_move(self.game, events)
            
            if col is not None and self.game.is_valid_location(col):
                self.game.drop_piece(self.current_player, col)
                if not self.game.is_game_over():
                    self.current_player = (self.current_player + 1) % len(self.agents)

    def run(self):
        running = True
        while running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
            
            if self.state == GameState.MENU:
                self.handle_menu_events(events)
                self.draw_menu()
            elif self.state == GameState.PLAYING:
                self.handle_game_events(events)
                self.draw_game()
            
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = GameManager()
    game.run()

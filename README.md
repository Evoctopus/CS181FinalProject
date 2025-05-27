# CS181FinalProject
ConnectFour.py contains the basical logic of the game, and GameManager.py is generate the game from ConnectFour.py logic and put the menu to select the different agent of the game.

In GameManager.py,

This controls the Agent select of player1 and player2.

self.menu_buttons= [

    {"text": "Human VS Human", "rect": pygame.Rect(250, 160, 200, 50), "agents": [HumanAgent(0, [0,1]), HumanAgent(1, [0,1])]},

    {"text": "Human VS Radom", "rect": pygame.Rect(250, 220, 200, 50), "agents": [HumanAgent(0, [0,1]), RandomAgent(1, [0,1])]},

    {"text": "Human vs MiniMax", "rect": pygame.Rect(250, 280, 200, 50), "agents": [HumanAgent(0, [0,1]), MiniMax(1, [0,1], 4, evaluate_func)]},

    {"text": "Human vs Greedy", "rect": pygame.Rect(250, 340, 200, 50), "agents": [HumanAgent(0, [0,1]), GreedyAgent(1, [0, 1], naive_greedy_reward)]},

    {"text": "Human vs Qlearning", "rect": pygame.Rect(250, 400, 200, 50), "agents": [HumanAgent(0, [0,1]), QLearningAgent(1, [0,1])]},

    {"text": "Exit", "rect": pygame.Rect(250, 460, 200, 50), "agents": None}

    ]What's more in the def draw_game(self), we draw the map and chess of the game.Anyway this def also controls the button of exit and restart for player to choosing during the game.

In Agent.py we trying to make different agent of the players,such as Human, Radom, Greedy, MiniMax, Greedy, and  Qlearning.

For the part of training Qlearning is in the Training.py. This part independents of the ConnectFour gaming.By changing

opponent_agent_class=GreedyAgent, and opponent=opponent_agent_class(1, team_sequence),we can use different agent in Agent.py to train the ai, and update the q_table for the result of training.

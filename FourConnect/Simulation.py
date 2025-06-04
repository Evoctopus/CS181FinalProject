from Agent import *
from MCT import *
from ConnectFour import ConnectFour

def stimulate(iteration, agents : list[Agent], rows=6, cols=7):
    wins = [0 for _ in range(len(agents))]
    draws = 0
    agentCnt = len(agents)
    for _ in range(iteration):

        game = ConnectFour(rows=rows, cols=cols)
        current_player = -1

        while not game.is_game_over():
            current_player = (current_player + 1) % agentCnt
            player = agents[current_player]
            col = player.make_move(game)
            game.drop_piece(current_player, col)
        
        if game.game_over:
            wins[current_player] += 1
        else:
            draws += 1
    
    for id in range(agentCnt):
        print(str(agents[id])+":", wins[id], "Win rate:", wins[id] / iteration)
    
    print("draw:", draws)
            



team_sequence = [0, 1]
random_agent_sente = RandomAgent(0, team_sequence)
greedy_agent_sente = GreedyAgent(0, team_sequence)
minimax_agent_sente = MiniMax(0, team_sequence, 4, evaluate_func)
mct_agent_sente = MCT_Agent(0, team_sequence)


random_agent_gote = RandomAgent(1, team_sequence)
greedy_agent_gote = GreedyAgent(1, team_sequence)
minimax_agent_gote = MiniMax(1, team_sequence, 4, evaluate_func) 
mct_agent_gote = MCT_Agent(1, team_sequence)
mct_agent_radom_gote =QLearningAgent(id=1, team_sequence=[0,1],model_path="qlearning_radom.pkl")
mct_agent_greedy_gote =QLearningAgent(id=1, team_sequence=[0,1],model_path="qlearning_greedy.pkl")
mct_agent_MCT_gote =QLearningAgent(id=1, team_sequence=[0,1],model_path="qlearning_MCT.pkl")
mct_agent_MiniMax_gote =QLearningAgent(id=1, team_sequence=[0,1],model_path="qlearning_MiniMax.pkl")

agents = [random_agent_sente, mct_agent_gote]
stimulate(50, agents)



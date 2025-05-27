from ConnectFour import ConnectFour
from Agent import *

def train_qlearning_agent(episodes=5000, opponent_agent_class=GreedyAgent, 
                         save_path="qlearning_model.pkl", verbose=True):
    """
    - episodes: training times
    - opponent_agent_class: training agent
    - save_path: path to save
    - verbose: is print or not
    """
    team_sequence = [0, 1]  # 0-self agent，1-another player agent
    q_agent = QLearningAgent(0, team_sequence)
    opponent = opponent_agent_class(1, team_sequence)   
    wins = 0
    losses = 0
    ties = 0
    
    for episode in range(episodes):
        game = ConnectFour()
        agents = [q_agent, opponent]
        current_player = 0
        game_history = []
        while not game.is_game_over():
            current_state = game.get_board_state()
            action = agents[current_player].make_move(game)
            if action is not None:
                row = game.drop_piece(current_player, action)
                if current_player == 0:  # only record player 1:Q-learning agent moves
                    game_history.append((current_state, action))
                current_player = 1 - current_player
            else:
                break
        
        if game.game_over:
            winner = None
            for row in range(game.rows):
                for col in range(game.cols):
                    if game.board[row][col] != -1:
                        if game.check_winning_move(row, col):
                            winner = game.board[row][col]
                            break
                if winner is not None:
                    break
            
            if winner == 0:  # self
                reward = 1
                wins += 1
            elif winner == 1:  
                reward = -1
                losses += 1
            else: 
                reward = 0
                ties += 1
        elif game.is_tie():
            reward = 0
            ties += 1
        else:
            reward = 0
        # update
        for i in range(len(game_history) - 1, -1, -1):
            state, action = game_history[i]
            
            if i == len(game_history) - 1:
                next_state = game.get_board_state()
                q_agent.update_q_table(state, action, reward, next_state, True)
            else:
                next_state, _ = game_history[i + 1]
                q_agent.update_q_table(state, action, 0, next_state, False)
            
            reward *= q_agent.gamma
        
        # change epsilon
        if episode > 0 and episode % 1000 == 0:
            q_agent.epsilon = max(0.01, q_agent.epsilon * 0.95)
            
            if verbose:
                win_rate = wins / (episode + 1) * 100
                print(f"Episode {episode}: Win Rate: {win_rate:.2f}%, "
                      f"Wins: {wins}, Losses: {losses}, Ties: {ties}, "
                      f"Epsilon: {q_agent.epsilon:.3f}")
    
    q_agent.save_q_table(save_path)
    q_agent.set_training_mode(False)

    return q_agent

if __name__ == "__main__":
    trained_agent = train_qlearning_agent(episodes=5000, verbose=True)

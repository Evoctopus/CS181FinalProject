import copy

class ConnectFour:
    def __init__(self, rows=6, cols=7):
        self.rows = rows
        self.cols = cols
        self.board = [[-1 for _ in range(cols)] for _ in range(rows)]
        self.game_over = False


    def drop_piece(self, current_player, col):
        if self.game_over or not self.is_valid_location(col):
            return None
       
        row = self.get_top_row(col)
        self.board[row][col] = current_player
        self.check_winning_move(row, col)

        return row


    def get_top_row(self, col):
        for row in range(self.rows - 1, -1, -1):
            if self.board[row][col] == -1:
                return row
  
    def is_valid_location(self, col):
        return 0 <= col < self.cols and self.board[0][col] == -1

    def check_winning_move(self, row, col, piece=None):
        if piece == None:
            piece = self.board[row][col]
        
        # Check horizontal
        for c in range(self.cols-3):
            if all(self.board[row][c+i] == piece for i in range(4)):
                self.game_over = True
                return True

        # Check vertical
        for r in range(self.rows-3):
            if all(self.board[r+i][col] == piece for i in range(4)):
                self.game_over = True
                return True

        # Check diagonal (down-right)
        for r in range(self.rows-3):
            for c in range(self.cols-3):
                if all(self.board[r+i][c+i] == piece for i in range(4)):
                    self.game_over = True
                    return True

        # Check diagonal (up-right)
        for r in range(3, self.rows):
            for c in range(self.cols-3):
                if all(self.board[r-i][c+i] == piece for i in range(4)):
                    self.game_over = True
                    return True

        return False

    def check_potential_win(self, row, col, piece):
        if row < 0:
            return False
        self.board[row][col] = piece
        success = self.check_winning_move(row, col, piece)
        self.game_over = False
        self.board[row][col] = -1
        return success

    def is_tie(self):
        return not self.game_over and all(self.board[0][c] != -1 for c in range(self.cols))

    def get_board_state(self):
        return [row[:] for row in self.board]

    def is_game_over(self):
        return self.game_over or self.is_tie()

    def get_chess(self, row, col):
        return self.board[row][col]

    def reset_game(self):
        self.board = [[-1 for _ in range(self.cols)] for _ in range(self.rows)]
        self.game_over = False 
    
    def get_legal_action(self):
        return [col for col in range(self.cols) if self.board[0][col] == -1]

    def get_next_state(self, col, id):
        tmp_game = copy.deepcopy(self)
        row = tmp_game.drop_piece(id, col)
        return tmp_game, row


    def __str__(self):
        board_str = ""
        for row in self.board:
            board_str += " | ".join(str(piece) if piece != -1 else "." for piece in row) + "\n"
        return board_str   
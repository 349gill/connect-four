# Implementing Connect Four on CLI
import random
import numpy as np
import copy


class Game:
    def __init__(self, difficulty) -> None:
        self.board = Board(6, 7)
        self.difficulty = difficulty


class Board:
    def __init__(self, rows, cols) -> None:
        self.position = np.full((rows, cols), "_")
        self.vacant_squares = rows*cols
        self.turn = 'O'
        self.last_move = 0, 0

    def state(self):
        if self.vacant_squares <= 0:
            return 1
        for i in range(self.position.shape[0]-1, -1, -1):
            for j in range(0, self.position.shape[1]):
                if j < self.position.shape[1]-3:
                    if self.position[i][j] == self.position[i][j+1] == self.position[i][j+2] == self.position[i][j+3] != '_':
                        return self.position[i][j]
                if i > 2:
                    if self.position[i][j] == self.position[i-1][j] == self.position[i-2][j] == self.position[i-3][j] != '_':
                        return self.position[i][j]
        x, y = self.last_move
        diag = np.diag(self.position, y-x)
        if diag.size >= 4:
            for i in range(diag.size-3):
                if diag[i] == diag[i+1] == diag[i+2] == diag[i+3] != '_':
                    return diag[i]
        opp_diag = np.diag(np.rot90(self.position), x+y-self.position.shape[0])
        if opp_diag.size >= 4:
            for i in range(opp_diag.size-3):
                if opp_diag[i] == opp_diag[i+1] == opp_diag[i+2] == opp_diag[i+3] != '_':
                    return diag[i]
        return 0

    def move(self, col):
        if col < self.position.shape[1] and self.position[0][col] == '_':
            for i in range(self.position.shape[0]-1, -1, -1):
                if self.position[i][col] == '_':
                    self.position[i][col] = self.turn
                    self.turn = 'X' if self.turn == 'O' else 'O'
                    self.last_move = i, col
                    return

    def rand(self):
        col = random.randrange(self.position.shape[1])
        if self.position[0][col] != '_':
            return self.rand()
        self.move(col)

    def score(self):
        score = 0
    # Minimax

    def minimax(self, board, depth, alpha, beta, maximizing):
        if self.state() == 1:
            return 0, None
        elif self.state() == 'O':
            return -1000, None
        elif self.state() == 'X':
            return 1000, None
        if depth == 0:
            return self.score(), None
        if maximizing == True:
            max_eval = -100000
            best_move = None

            for col in range(0, self.position.shape[1]):
                if self.position[0][col] == '_':
                    temp = copy.deepcopy(board)
                    temp.move(col)
                    eval = self.minimax(temp, depth-1, alpha, beta, False)[0]
                    if eval > max_eval:
                        max_eval = eval
                        best_move = col
                    alpha = max(alpha, max_eval)
                    if alpha >= beta:
                        break
            return max_eval, best_move
        elif maximizing == False:
            min_eval = 100000
            best_move = None

            for col in range(0, self.position.shape[1]):
                if self.position[0][col] == '_':
                    temp = copy.deepcopy(board)
                    temp.move(col)
                    eval = self.minimax(temp, depth-1, alpha, beta, True)[0]
                    if eval < min_eval:
                        max_eval = eval
                        best_move = col
                    beta = min(beta, min_eval)
                    if alpha >= beta:
                        break
            return min_eval, best_move


def main():
    game = Game(0)
    current_state = 0
    print("Connect Four!")
    print(game.board.position)
    while current_state == 0:
        if game.board.turn == 'O':
            game.board.move(int(input("Your turn, pick a column(0-7)!")))
            print(game.board.position)
            game.board.vacant_squares -= 1
            current_state = game.board.state()
            if current_state != 0:
                break
        if game.board.turn == 'X':
            game.board.rand()
            print(game.board.position)
            game.board.vacant_squares -= 1
            current_state = game.board.state()
    if current_state == 1:
        print("Draw!")
    else:
        print(current_state + ' Has Won!')


main()

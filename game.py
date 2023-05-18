# Implementing Connect Four on CLI
import random
import numpy as np
import time


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
                if j < self.position.shape[0]-3:
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
                    self.vacant_squares -= 1
                    print(f"{self.turn} marked {i},{col}")
                    self.turn = 'X' if self.turn == 'O' else 'O'
                    self.last_move = i, col
                    return
        self.move(int(input(str(col)+" is an invalid move, try again!")))

    def rand(self):
        col = random.randrange(self.position.shape[1])
        if self.position[0][col] != '_':
            return self.rand()
        self.move(col)

    def minimax(self):
        pass

    def negamax(self):
        pass


def main():
    game = Game(0)
    current_state = 0
    print("Connect Four!")
    print(game.board.position)
    while current_state == 0:
        if game.board.turn == 'O':
            game.board.move(int(input("Your turn, pick a column(0-7)!")))
            print(game.board.position)
            current_state = game.board.state()
            if current_state != 0:
                break
        if game.board.turn == 'X':
            game.board.rand()
            time.sleep(0.75)
            print(game.board.position)
            current_state = game.board.state()
    if current_state == 1:
        print("Draw!")
    else:
        print(current_state + ' Has Won!')


main()

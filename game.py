class Game:
    def __init__(self, id: int):
        self.moves = 0
        self.ready = False  # for connection
        self.id = id
        self.curr_values = [None, None]
        self.cells_values = [-1] * 9

    def get_player_value(self, player: int) -> int:
        return self.curr_values[player]

    def empty_cells(self):
        return -1 in self.cells_values

    def connected(self):
        return self.ready

    def reset_moves(self):
        self.moves = (self.moves + 1) % 2

    def reset_cells(self):
        self.cells_values = [-1] * 9

    def play(self, player: int, value: int):  # move: [0 .. 8]
        self.curr_values[player] = value
        self.cells_values[value] = player
        self.reset_moves()      # if you lose next round you play first

    def win_game(self):
        winner_player = -1
        cells = self.cells_values
        if cells[0] == cells[4] == cells[8] or cells[1] == cells[4] == cells[7] or \
                cells[2] == cells[4] == cells[6] or cells[3] == cells[4] == cells[5] and cells[4] != -1:
            winner_player = cells[4]
        elif cells[0] == cells[1] == cells[2] or cells[0] == cells[3] == cells[6] and cells[0] != -1:
            winner_player = cells[0]
        elif cells[2] == cells[5] == cells[8] or cells[6] == cells[7] == cells[8] and cells[8] != -1:
            winner_player = cells[8]
        return winner_player

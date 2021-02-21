from Chess import *


class Chessboard:
    def __init__(self):
        self.board = [[0 for i in range(8)] for j in range(8)]

    def reset(self):
        self.board = [[0 for i in range(8)] for j in range(8)]


class Player:
    def __init__(self, side, board):
        self.side = side
        self.board = board
        self.passant = None
        self.pieces = []
        for i in range(8):
            self.pieces.append(Pawn(self.side, i, self, self.board))
        for i in range(2):
            self.pieces.append(Knight(self.side, i, self, self.board))
        for i in range(2):
            self.pieces.append(Bishop(self.side, i, self, self.board))
        for i in range(2):
            self.pieces.append(Rook(self.side, i, self, self.board))
        for i in range(1):
            self.pieces.append(Queen(self.side, i, self, self.board))
        for i in range(1):
            self.pieces.append(King(self.side, i, self, self.board))

    def depassant(self):
        if self.passant:
            self.passant.passant = 0
            self.passant = None


class Game:
    def __init__(self):
        self.board = Chessboard()
        self.black = Player(0, self.board)
        self.white = Player(1, self.board)
        self.state = State()
        self.state.connect_chessboard(self.board)
        self.hold = None

    def step_state(self, start, end, dead=None):
        self.state = self.state.step(start, end, dead)
        if self.turn() % 2 == 1:
            self.white.depassant()
        else:
            self.black.depassant()

    def backward(self):
        if self.state.previous:
            self.state = self.state.backward()

    def forward(self):
        if self.state.next:
            self.state = self.state.forward()

    def turn(self):
        return self.state.TURN

    def start(self):
        return self.state.start

    def end(self):
        return self.state.end

    def previous(self):
        return self.state.previous

    def next(self):
        return self.state.next

    def killed(self):
        return self.state.dead

ROW = "87654321"
COL = "ABCDEFGH"
SIDE = ["_b", "_w"]


class Piece:
    def __init__(self):
        self.cls = None
        self.side = None
        self.number = None
        self.player = None
        self.chessboard = None
        self.y, self.x = [None, None]
        self.status = 1
        self.hold = 0

    def step(self, y, x):
        movable = self.check_moves()
        if [y, x] in movable:
            
            if self.chessboard.board[y][x]:
                self.chessboard.board[y][x].dead()
                self.set_position(y, x)

            else:
                self.set_position(y, x)

    def check_moves(self):
        raise NotImplementedError("Not overridden")

    def dead(self):
        self.status = 0
        self.remove()

    def alive(self):
        self.status = 1
        self.update_board()

    def set_position(self, y, x):
        self.remove()
        self.y = y
        self.x = x
        self.update_board()

    def update_board(self):
        self.chessboard.board[self.y][self.x] = self

    def remove(self):
        self.chessboard.board[self.y][self.x] = 0

    def check_teammate(self, piece):
        return self.side == piece.side

    def held(self):
        self.hold = 1
        return self

    def unheld(self):
        self.hold = 0


class Pawn(Piece):
    def __init__(self, side, number, player, chessboard):
        super().__init__()
        self.cls = "Pawn"
        self.side = side
        self.number = number
        self.player = player
        self.chessboard = chessboard
        self.passant = 0
        if self.side == 0:
            self.y, self.x = [1, number]
        elif self.side == 1:
            self.y, self.x = [6, number]
        self.update_board()

    def step(self, y, x):
        movable = self.check_moves()
        passant = []
        print(self.check_passant())
        if self.side == 0:
            if self.y == 4:
                passant = self.check_passant()
        elif self.side == 1:
            if self.y == 3:
                passant = self.check_passant()

        if [y, x] in movable:
            if self.chessboard.board[y][x]:
                self.chessboard.board[y][x].dead()
                self.set_position(y, x)

            else:
                if self.side == 0:
                    if y - self.y == 2:
                        self.be_passant()
                elif self.side == 1:
                    if self.y - y == 2:
                        self.be_passant()
                self.set_position(y, x)

        elif [y, x] in passant:
            print("yes")
            if self.side == 0:
                self.chessboard.board[y - 1][x].dead()
                self.set_position(y, x)

            elif self.side == 1:
                self.chessboard.board[y + 1][x].dead()
                self.set_position(y, x)
        else:
            print("this:", [y, x])
            print("p:", passant)
            print("no")


    def check_moves(self):
        movable = []
        if self.side == 0:
            if self.y + 1 <= 7:
                if not self.chessboard.board[self.y + 1][self.x]:
                    movable.append([self.y + 1, self.x])
                if self.y == 1:
                    if not self.chessboard.board[self.y + 1][self.x]:
                        if not self.chessboard.board[self.y + 2][self.x]:
                            movable.append([self.y + 2, self.x])
                if self.x + 1 <= 7:
                    if self.chessboard.board[self.y + 1][self.x + 1]:
                        if not self.check_teammate(self.chessboard.board[self.y + 1][self.x + 1]):
                            movable.append([self.y + 1, self.x + 1])
                if self.x - 1 >= 0:
                    if self.chessboard.board[self.y + 1][self.x - 1]:
                        if not self.check_teammate(self.chessboard.board[self.y + 1][self.x - 1]):
                            movable.append([self.y + 1, self.x - 1])

        elif self.side == 1:
            if self.y - 1 >= 0:
                if not self.chessboard.board[self.y - 1][self.x]:
                    movable.append([self.y - 1, self.x])
                if self.y == 6:
                    if not self.chessboard.board[self.y - 1][self.x]:
                        if not self.chessboard.board[self.y - 2][self.x]:
                            movable.append([self.y - 2, self.x])
                if self.x + 1 <= 7:
                    if self.chessboard.board[self.y - 1][self.x + 1]:
                        if not self.check_teammate(self.chessboard.board[self.y - 1][self.x + 1]):
                            movable.append([self.y - 1, self.x + 1])
                if self.x - 1 >= 0:
                    if self.chessboard.board[self.y - 1][self.x - 1]:
                        if not self.check_teammate(self.chessboard.board[self.y - 1][self.x - 1]):
                            movable.append([self.y - 1, self.x - 1])

        moves = []
        for [j, i] in movable:
            if not self.chessboard.board[j][i]:
                moves.append([j, i])
            elif not self.check_teammate(self.chessboard.board[j][i]):
                moves.append([j, i])

        return moves

    def check_passant(self):
        passant_move = []
        if self.side == 0:
            if self.y == 4:
                if self.x + 1 <= 7:
                    that = self.chessboard.board[self.y][self.x + 1]
                    if that:
                        if not self.check_teammate(that):
                            if that.cls == "Pawn":
                                if that.passant:
                                    passant_move.append([self.y + 1, self.x + 1])
                if self.x - 1 >= 0:
                    that = self.chessboard.board[self.y][self.x - 1]
                    if that:
                        if not self.check_teammate(that):
                            if that.cls == "Pawn":
                                if that.passant:
                                    passant_move.append([self.y + 1, self.x - 1])

        elif self.side == 1:
            if self.y == 3:
                if self.x + 1 <= 7:
                    that = self.chessboard.board[self.y][self.x + 1]
                    if that:
                        if not self.check_teammate(that):
                            if that.cls == "Pawn":
                                if that.passant:
                                    passant_move.append([self.y - 1, self.x + 1])
                if self.x - 1 >= 0:
                    that = self.chessboard.board[self.y][self.x - 1]
                    if that:
                        if not self.check_teammate(that):
                            if that.cls == "Pawn":
                                if that.passant:
                                    passant_move.append([self.y - 1, self.x - 1])

        return passant_move

    def be_passant(self):
        self.passant = 1
        self.player.passant = self

    def promotion(self, number):
        pass

    def __str__(self):
        return "pawn" + SIDE[self.side]


class Knight(Piece):
    def __init__(self, side, number, player, chessboard, position=None):
        super().__init__()
        self.cls = "Knight"
        self.side = side
        self.number = number
        self.player = player
        self.chessboard = chessboard
        if not position:
            if self.side == 0:
                if self.number == 0:
                    self.y, self.x = [0, 1]
                else:
                    self.y, self.x = [0, 6]
            elif self.side == 1:
                if self.number == 0:
                    self.y, self.x = [7, 1]
                else:
                    self.y, self.x = [7, 6]
        else:
            self.y, self.x = position
        self.update_board()


    def check_moves(self):
        movable = []
        if self.y - 1 >= 0:
            if self.x - 2 >= 0:
                movable.append([self.y - 1, self.x - 2])
            if self.x + 2 <= 7:
                movable.append([self.y - 1, self.x + 2])
            if self.y - 2 >= 0:
                if self.x - 1 >= 0:
                    movable.append([self.y - 2, self.x - 1])
                if self.x + 1 <= 7:
                    movable.append([self.y - 2, self.x + 1])
        if self.y + 1 <= 7:
            if self.x - 2 >= 0:
                movable.append([self.y + 1, self.x - 2])
            if self.x + 2 <= 7:
                movable.append([self.y + 1, self.x + 2])
            if self.y + 2 <= 7:
                if self.x - 1 >= 0:
                    movable.append([self.y + 2, self.x - 1])
                if self.x + 1 <= 7:
                    movable.append([self.y + 2, self.x + 1])

        moves = []
        for [j, i] in movable:
            if not self.chessboard.board[j][i]:
                moves.append([j, i])
            elif not self.check_teammate(self.chessboard.board[j][i]):
                moves.append([j, i])

        return moves

    def __str__(self):
        return "knight" + SIDE[self.side]


class Bishop(Piece):
    def __init__(self, side, number, player, chessboard, position=None):
        super().__init__()
        self.cls = "Bishop"
        self.side = side
        self.number = number
        self.player = player
        self.chessboard = chessboard
        if not position:
            if self.side == 0:
                if self.number == 0:
                    self.y, self.x = [0, 2]
                else:
                    self.y, self.x = [0, 5]
            elif self.side == 1:
                if self.number == 0:
                    self.y, self.x = [7, 2]
                else:
                    self.y, self.x = [7, 5]
        else:
            self.y, self.x = position
        self.update_board()

    def check_moves(self):
        movable = []
        block = [0, 0, 0, 0]
        for i in range(1, 8):
            if self.y + i <= 7:
                if self.x + i <= 7:
                    if not block[0]:
                        movable.append([self.y + i, self.x + i])
                        if self.chessboard.board[self.y + i][self.x + i]:
                            block[0] = 1
                if self.x - i >= 0:
                    if not block[1]:
                        movable.append([self.y + i, self.x - i])
                        if self.chessboard.board[self.y + i][self.x - i]:
                            block[1] = 1
            if self.y - i >= 0:
                if self.x + i <= 7:
                    if not block[2]:
                        movable.append([self.y - i, self.x + i])
                        if self.chessboard.board[self.y - i][self.x + i]:
                            block[2] = 1
                if self.x - i >= 0:
                    if not block[3]:
                        movable.append([self.y - i, self.x - i])
                        if self.chessboard.board[self.y - i][self.x - i]:
                            block[3] = 1

        moves = []
        for [j, i] in movable:
            if not self.chessboard.board[j][i]:
                moves.append([j, i])
            elif not self.check_teammate(self.chessboard.board[j][i]):
                moves.append([j, i])

        return moves

    def __str__(self):
        return "bishop" + SIDE[self.side]


class Rook(Piece):
    def __init__(self, side, number, player, chessboard, position=None):
        super().__init__()
        self.cls = "Rook"
        self.side = side
        self.number = number
        self.player = player
        self.chessboard = chessboard
        if not position:
            if self.side == 0:
                if self.number == 0:
                    self.y, self.x = [0, 0]
                else:
                    self.y, self.x = [0, 7]
            elif self.side == 1:
                if self.number == 0:
                    self.y, self.x = [7, 0]
                else:
                    self.y, self.x = [7, 7]
        else:
            self.y, self.x = position
        self.update_board()

    def check_moves(self):
        movable = []
        block = [0, 0, 0, 0]
        for j in range(1, 8):
            if self.y + j <= 7:
                if not block[0]:
                    movable.append([self.y + j, self.x])
                    if self.chessboard.board[self.y + j][self.x]:
                        block[0] = 1
            if self.y - j >= 0:
                if not block[1]:
                    movable.append([self.y - j, self.x])
                    if self.chessboard.board[self.y - j][self.x]:
                        block[1] = 1
        for i in range(1, 8):
            if self.x + i <= 7:
                if not block[2]:
                    movable.append([self.y, self.x + i])
                    if self.chessboard.board[self.y][self.x + i]:
                        block[2] = 1
            if self.x - i >= 0:
                if not block[3]:
                    movable.append([self.y, self.x - i])
                    if self.chessboard.board[self.y][self.x - i]:
                        block[3] = 1

        moves = []
        for [j, i] in movable:
            if not self.chessboard.board[j][i]:
                moves.append([j, i])
            elif not self.check_teammate(self.chessboard.board[j][i]):
                moves.append([j, i])

        return moves

    def __str__(self):
        return "rook" + SIDE[self.side]


class Queen(Piece):
    def __init__(self, side, number, player, chessboard, position=None):
        super().__init__()
        self.cls = "Queen"
        self.side = side
        self.number = number
        self.player = player
        self.chessboard = chessboard
        if not position:
            if self.side == 0:
                self.y, self.x = [0, 3]
            elif self.side == 1:
                self.y, self.x = [7, 3]
        else:
            self.y, self.x = position
        self.update_board()

    def check_moves(self):
        movable = []
        block_1 = [0, 0, 0, 0]
        block_2 = [0, 0, 0, 0]
        for i in range(1, 8):
            if self.y + i <= 7:
                if self.x + i <= 7:
                    if not block_1[0]:
                        movable.append([self.y + i, self.x + i])
                        if self.chessboard.board[self.y + i][self.x + i]:
                            block_1[0] = 1
                if self.x - i >= 0:
                    if not block_1[1]:
                        movable.append([self.y + i, self.x - i])
                        if self.chessboard.board[self.y + i][self.x - i]:
                            block_1[1] = 1
            if self.y - i >= 0:
                if self.x + i <= 7:
                    if not block_1[2]:
                        movable.append([self.y - i, self.x + i])
                        if self.chessboard.board[self.y - i][self.x + i]:
                            block_1[2] = 1
                if self.x - i >= 0:
                    if not block_1[3]:
                        movable.append([self.y - i, self.x - i])
                        if self.chessboard.board[self.y - i][self.x - i]:
                            block_1[3] = 1

        for j in range(1, 8):
            if self.y + j <= 7:
                if not block_2[0]:
                    movable.append([self.y + j, self.x])
                    if self.chessboard.board[self.y + j][self.x]:
                        block_2[0] = 1
            if self.y - j >= 0:
                if not block_2[1]:
                    movable.append([self.y - j, self.x])
                    if self.chessboard.board[self.y - j][self.x]:
                        block_2[1] = 1
        for i in range(1, 8):
            if self.x + i <= 7:
                if not block_2[2]:
                    movable.append([self.y, self.x + i])
                    if self.chessboard.board[self.y][self.x + i]:
                        block_2[2] = 1
            if self.x - i >= 0:
                if not block_2[3]:
                    movable.append([self.y, self.x - i])
                    if self.chessboard.board[self.y][self.x - i]:
                        block_2[3] = 1

        for j in range(-1, 2):
            for i in range(-1, 2):
                if j != 0 or i != 0:
                    if 0 <= self.y + j <= 7 and 0 <= self.x + i <= 7:
                        if [self.y + j, self.x + i] not in movable:
                            movable.append([self.y + j, self.x + i])

        moves = []
        for [j, i] in movable:
            print([j, i])
            if not self.chessboard.board[j][i]:
                moves.append([j, i])
            elif not self.check_teammate(self.chessboard.board[j][i]):
                moves.append([j, i])

        return moves

    def __str__(self):
        return "queen" + SIDE[self.side]


class King(Piece):
    def __init__(self, side, number, player, chessboard, position=None):
        super().__init__()
        self.cls = "King"
        self.side = side
        self.number = number
        self.player = player
        self.chessboard = chessboard
        if not position:
            if self.side == 0:
                self.y, self.x = [0, 4]
            elif self.side == 1:
                self.y, self.x = [7, 4]
        else:
            self.y, self.x = position
        self.update_board()

    def check_moves(self):
        movable = []
        for j in range(-1, 2):
            for i in range(-1, 2):
                if j != 0 or i != 0:
                    if 0 <= self.y + j <= 7 and 0 <= self.x + i <= 7:
                        movable.append([self.y + j, self.x + i])

        moves = []
        for [j, i] in movable:
            if not self.chessboard.board[j][i]:
                moves.append([j, i])
            elif not self.check_teammate(self.chessboard.board[j][i]):
                moves.append([j, i])
        
        return moves

    def __str__(self):
        return "king" + SIDE[self.side]


class State:

    board = None
    TURN = 0

    def __init__(self, start=None, end=None, previous=None, dead=None):
        State.plus()
        self.start = start
        self.end = end
        self.previous = previous
        self.dead = dead
        self.next = None

    @classmethod
    def connect_chessboard(cls, chessboard):
        cls.board = chessboard

    @classmethod
    def plus(cls):
        cls.TURN += 1

    @classmethod
    def minus(cls):
        cls.TURN -= 1

    @classmethod
    def reset_turn(cls):
        cls.TURN = 0

    def step(self, start, end, dead=None):
        new_state = State(start, end, self, dead=dead)
        self.next = new_state
        return new_state

    def backward(self):
        if State.board:
            if self.previous:
                '''put back the piece'''
                State.minus()
                State.board.board[self.start[0]][self.start[1]] = State.board.board[self.end[0]][self.end[1]]
                State.board.board[self.end[0]][self.end[1]].remove()
                State.board.board[self.start[0]][self.start[1]].set_position(self.start[0], self.start[1])
                if self.dead:
                    self.dead.alive()

                return self.previous

    def forward(self):
        if State.board:
            if self.next:
                '''put back the piece'''
                State.plus()
                next_state = self.next
                State.board.board[next_state.start[0]][next_state.start[1]].step(next_state.end[0], next_state.end[1])
                return self.next


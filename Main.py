import os
import pygame
import keyboard
import time
from Game import *


BLOCK = 100
WIDTH = BLOCK * 8
HEIGHT = BLOCK * 8
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess")

FPS = 24

IMAGE_DICT = os.path.join(os.getcwd(), "images")

BOARD_IMG_ODD = os.path.join(IMAGE_DICT, "square_coffee.png")
BOARD_IMG_ODD = pygame.image.load(BOARD_IMG_ODD)
BOARD_ODD = pygame.transform.scale(BOARD_IMG_ODD, (BLOCK, BLOCK))

BOARD_IMG_EVEN = os.path.join(IMAGE_DICT, "square_brown.png")
BOARD_IMG_EVEN = pygame.image.load(BOARD_IMG_EVEN)
BOARD_EVEN = pygame.transform.scale(BOARD_IMG_EVEN, (BLOCK, BLOCK))

PIECE_WIDTH = 90
PIECE_HEIGHT = 100
W_OFFSET = 10
PIECES = ["pawn_b", "knight_b", "bishop_b", "rook_b", "queen_b", "king_b", "pawn_w", "knight_w", "bishop_w", "rook_w", "queen_w", "king_w"]
PAWN_B = pygame.transform.scale(pygame.image.load(os.path.join(IMAGE_DICT, PIECES[0] + ".png")), (PIECE_WIDTH, PIECE_HEIGHT))
KNIGHT_B = pygame.transform.scale(pygame.image.load(os.path.join(IMAGE_DICT, PIECES[1] + ".png")), (PIECE_WIDTH, PIECE_HEIGHT))
BISHOP_B = pygame.transform.scale(pygame.image.load(os.path.join(IMAGE_DICT, PIECES[2] + ".png")), (PIECE_WIDTH, PIECE_HEIGHT))
ROOK_B = pygame.transform.scale(pygame.image.load(os.path.join(IMAGE_DICT, PIECES[3] + ".png")), (PIECE_WIDTH, PIECE_HEIGHT))
QUEEN_B = pygame.transform.scale(pygame.image.load(os.path.join(IMAGE_DICT, PIECES[4] + ".png")), (PIECE_WIDTH, PIECE_HEIGHT))
KING_B = pygame.transform.scale(pygame.image.load(os.path.join(IMAGE_DICT, PIECES[5] + ".png")), (PIECE_WIDTH, PIECE_HEIGHT))
PAWN_W = pygame.transform.scale(pygame.image.load(os.path.join(IMAGE_DICT, PIECES[6] + ".png")), (PIECE_WIDTH, PIECE_HEIGHT))
KNIGHT_W = pygame.transform.scale(pygame.image.load(os.path.join(IMAGE_DICT, PIECES[7] + ".png")), (PIECE_WIDTH, PIECE_HEIGHT))
BISHOP_W = pygame.transform.scale(pygame.image.load(os.path.join(IMAGE_DICT, PIECES[8] + ".png")), (PIECE_WIDTH, PIECE_HEIGHT))
ROOK_W = pygame.transform.scale(pygame.image.load(os.path.join(IMAGE_DICT, PIECES[9] + ".png")), (PIECE_WIDTH, PIECE_HEIGHT))
QUEEN_W = pygame.transform.scale(pygame.image.load(os.path.join(IMAGE_DICT, PIECES[10] + ".png")), (PIECE_WIDTH, PIECE_HEIGHT))
KING_W = pygame.transform.scale(pygame.image.load(os.path.join(IMAGE_DICT, PIECES[11] + ".png")), (PIECE_WIDTH, PIECE_HEIGHT))
PIECES_DICT = {
    "pawn_b": PAWN_B, "knight_b": KNIGHT_B, "bishop_b": BISHOP_B, "rook_b": ROOK_B, "queen_b": QUEEN_B, "king_b": KING_B,
    "pawn_w": PAWN_W, "knight_w": KNIGHT_W, "bishop_w": BISHOP_W, "rook_w": ROOK_W, "queen_w": QUEEN_W, "king_w": KING_W
}

BlACK = (0, 0, 0)
WHITE = (255, 255, 255)
ORANGE = (255, 105, 0)
YELLOW = (255, 195, 77)
RED = (255, 0, 0)

PIECE_WIDTH = 100
PIECE_HEIGHT = 100


game = Game()


def draw_line():
    for i in range(9):
        pygame.draw.line(WINDOW, BlACK, (i * BLOCK, 0), (i * BLOCK, HEIGHT), 3)
        pygame.draw.line(WINDOW, BlACK, (0, i * BLOCK), (WIDTH, i * BLOCK), 3)


def draw_rect(y, x, width, height, color):
    pygame.draw.rect(WINDOW, color, [x * BLOCK, y * BLOCK, width, height])


def draw_window():
    WINDOW.fill(WHITE)
    for j in range(4):
        for i in range(4):
            WINDOW.blit(BOARD_IMG_ODD, (BLOCK * i * 2, BLOCK * j * 2))
            WINDOW.blit(BOARD_IMG_EVEN, (BLOCK * i * 2 + BLOCK, BLOCK * j * 2))

            WINDOW.blit(BOARD_IMG_EVEN, (BLOCK * i * 2, BLOCK * j * 2 + BLOCK))
            WINDOW.blit(BOARD_IMG_ODD, (BLOCK * i * 2 + BLOCK, BLOCK * j * 2 + BLOCK))

    if game.hold:
        draw_rect(game.hold.y, game.hold.x, BLOCK, BLOCK, YELLOW)
        for j, i in game.hold.check_moves():
            draw_rect(j, i, BLOCK, BLOCK, ORANGE)
        if game.hold.cls == "Pawn":
            for j, i in game.hold.check_passant():
                draw_rect(j, i, BLOCK, BLOCK, RED)

    draw_line()

    for piece in game.black.pieces:
        if piece.status:
            if not piece.hold:
                WINDOW.blit(PIECES_DICT[str(piece)], (piece.x * BLOCK + 7, piece.y * BLOCK))

    for piece in game.white.pieces:
        if piece.status:
            if not piece.hold:
                WINDOW.blit(PIECES_DICT[str(piece)], (piece.x * BLOCK + 7, piece.y * BLOCK))

    if game.hold:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        WINDOW.blit(PIECES_DICT[str(game.hold)], (mouse_x - PIECE_WIDTH / 2 + W_OFFSET, mouse_y - PIECE_HEIGHT / 2))

    pygame.display.update()


on_hold = None


def release():
    global on_hold
    if on_hold:
        on_hold.unheld()
        on_hold = None
        game.hold = None


def main():
    global game, on_hold
    clock = pygame.time.Clock()

    active = True
    while active:
        clock.tick(FPS)
        if keyboard.is_pressed("q"):
            active = False
            break
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                active = False
                break

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if on_hold:

                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        y, x = mouse_y // 100, mouse_x // 100
                        killed = None
                        if [y, x] in on_hold.check_moves():
                            if game.board.board[y][x]:
                                killed = game.board.board[y][x]
                            game.step_state(start=[on_hold.y, on_hold.x], end=[y, x], dead=killed)
                            on_hold.step(y, x)

                        elif on_hold.cls == "Pawn":
                            if [y, x] in on_hold.check_passant():
                                if on_hold.side == 0:
                                    if on_hold.y == 4:
                                        killed = game.board.board[y - 1][x]
                                elif on_hold.side == 1:
                                    if on_hold.y == 3:
                                        killed = game.board.board[y + 1][x]
                                game.step_state(start=[on_hold.y, on_hold.x], end=[y, x], dead=killed)
                                on_hold.step(y, x)

                        release()
                        print("killed:", killed)
                        if killed:
                            print("position:", killed.y, killed.x)
                        for i in game.board.board:
                            print(i)
                        print("black:", game.black.passant)
                        print("white:", game.white.passant)

                        # else:
                        #     if on_hold.cls == "Pawn":
                        #         if [y, x] in on_hold.check_passant():
                        #             if on_hold.side == 0:
                        #                 if on_hold.y == 4:
                        #                     killed = game.white.passant
                        #                     game.step_state(start=[on_hold.y, on_hold.x], end=[y, x], dead=killed)
                        #                     on_hold.step(y, x)
                        #
                        #             elif on_hold.side == 1:
                        #                 if on_hold.y == 3:
                        #                     if [y, x] in on_hold.check_passant():
                        #                         killed = game.black.passant
                        #                         game.step_state(start=[on_hold.y, on_hold.x], end=[y, x], dead=killed)
                        #                         on_hold.step(y, x)
                        #     release()

        if keyboard.is_pressed("r"):
            release()
            for i in game.board.board:
                print(i)
            State.reset_turn()
            game.board.reset()
            print("\n")
            for i in game.board.board:
                print(i)
            game = Game()
            print("\n")
            for i in game.board.board:
                print(i)
            time.sleep(0.1)

        if keyboard.is_pressed("w"):
            release()
            game.backward()
            # print("turn:", game.turn())
            # print("start:", game.start())
            # print("end:", game.end())
            # print("killed:", game.killed())
            # print("previous:", game.previous())
            # print("next:", game.next())
            # print("hold:", game.hold)
            # print("\n")
            time.sleep(0.1)

        if keyboard.is_pressed("e"):
            release()
            game.forward()
            # print("turn:", game.turn())
            # print("start:", game.start())
            # print("end:", game.end())
            # print("killed:", game.killed())
            # print("previous:", game.previous())
            # print("next:", game.next())
            # print("hold:", game.hold)
            # print("\n")
            time.sleep(0.1)


        mouse_pressed = pygame.mouse.get_pressed(3)[0]
        player = game.turn() % 2

        if mouse_pressed:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            y, x = mouse_y // 100, mouse_x // 100
            # print("turn:", game.turn())
            # print("start:", game.start())
            # print("end:", game.end())
            # print("killed:", game.killed())
            # print("previous:", game.previous())
            # print("next:", game.next())
            # print("hold:", game.hold)
            # print("\n")

            if not on_hold:
                if game.board.board[y][x]:
                    if game.board.board[y][x].side == player:
                        # print(game.board.board[y][x])
                        on_hold = game.board.board[y][x].held()
                        game.hold = game.board.board[y][x]

        draw_window()

    pygame.quit()


if __name__ == "__main__":
    main()
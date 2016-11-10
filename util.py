from functools import reduce
from itertools import cycle
import random

import chess
from ai import adversarial_search
from chess import Move
import weight as weight_mod



def white_minus_black(func):
    def decorated(*args, **kwargs):
        return func(chess.WHITE, *args, **kwargs) - func(chess.BLACK, *args, **kwargs)
    return decorated


def num_kings(board):
    return len([True for p in board.pieces if p == chess.KING])


class BoardException(Exception):
    board = None


def possible_actions(board):
    if board.is_game_over():
        return []
    else:
        actions = list(board.legal_moves)
        random.shuffle(actions)
        return actions

def step(board, move):
    new_board = chess.Bitboard(board.fen())
    new_board.push(move)
    return new_board

def toInt(spotToConvert):
    if spotToConvert == 'a1':
        return 0
    elif spotToConvert == 'b1':
        return 1
    elif spotToConvert == 'c1':
        return 2
    elif spotToConvert == 'd1':
        return 3
    elif spotToConvert == 'e1':
        return 4
    elif spotToConvert == 'f1':
        return 5
    elif spotToConvert == 'g1':
        return 6
    elif spotToConvert == 'h1':
        return 7
    elif spotToConvert == 'a2':
        return 8
    elif spotToConvert == 'b2':
        return 9
    elif spotToConvert == 'c2':
        return 10
    elif spotToConvert == 'd2':
        return 11
    elif spotToConvert == 'e2':
        return 12
    elif spotToConvert == 'f2':
        return 13
    elif spotToConvert == 'g2':
        return 14
    elif spotToConvert == 'h2':
        return 15
    elif spotToConvert == 'a3':
        return 16
    elif spotToConvert == 'b3':
        return 17
    elif spotToConvert == 'c3':
        return 18
    elif spotToConvert == 'd3':
        return 19
    elif spotToConvert == 'e3':
        return 20
    elif spotToConvert == 'f3':
        return 21
    elif spotToConvert == 'g3':
        return 22
    elif spotToConvert == 'h3':
        return 23
    elif spotToConvert == 'a4':
        return 24
    elif spotToConvert == 'b4':
        return 25
    elif spotToConvert == 'c4':
        return 26
    elif spotToConvert == 'd4':
        return 27
    elif spotToConvert == 'e4':
        return 28
    elif spotToConvert == 'f4':
        return 29
    elif spotToConvert == 'g4':
        return 30
    elif spotToConvert == 'h4':
        return 31
    elif spotToConvert == 'a5':
        return 32
    elif spotToConvert == 'b5':
        return 33
    elif spotToConvert == 'c5':
        return 34
    elif spotToConvert == 'd5':
        return 35
    elif spotToConvert == 'e5':
        return 36
    elif spotToConvert == 'f5':
        return 37
    elif spotToConvert == 'g5':
        return 38
    elif spotToConvert == 'h5':
        return 39
    elif spotToConvert == 'a6':
        return 40
    elif spotToConvert == 'b6':
        return 41
    elif spotToConvert == 'c6':
        return 42
    elif spotToConvert == 'd6':
        return 43
    elif spotToConvert == 'e6':
        return 44
    elif spotToConvert == 'f6':
        return 45
    elif spotToConvert == 'g6':
        return 46
    elif spotToConvert == 'h6':
        return 47
    elif spotToConvert == 'a7':
        return 48
    elif spotToConvert == 'b7':
        return 49
    elif spotToConvert == 'c7':
        return 50
    elif spotToConvert == 'd7':
        return 51
    elif spotToConvert == 'e7':
        return 52
    elif spotToConvert == 'f7':
        return 53
    elif spotToConvert == 'g7':
        return 54
    elif spotToConvert == 'h7':
        return 55
    elif spotToConvert == 'a8':
        return 56
    elif spotToConvert == 'b8':
        return 57
    elif spotToConvert == 'c8':
        return 58
    elif spotToConvert == 'd8':
        return 59
    elif spotToConvert == 'e8':
        return 60
    elif spotToConvert == 'f8':
        return 61
    elif spotToConvert == 'g8':
        return 62
    elif spotToConvert == 'h8':
        return 63

def readMoveFromFileX(board):
    Xlog = open("log_X.txt", "r")
    lineList = Xlog.readlines()
    line = lineList[len(lineList)-1]
    string = line[2] + line[4] + line[5]

    board.push_san(string)
    
    return True

def readMoveFromFileY(board):
    Ylog = open("log_Y.txt", "r")
    lineList = Ylog.readlines()
    line = lineList[len(lineList)-1]
    string = line[2] + line[4] + line[5]

    board.push_san(string)
    
    return True

def writeMoveToXFile(move, board, player):
    Xlog = open("log_X.txt", "a")
    Xlog.write(player)
    if board.piece_type_at(move.from_square) == 4:
        Xlog.write("R:")
    elif board.piece_type_at(move.from_square) == 2:
        Xlog.write("N:")
    elif board.piece_type_at(move.from_square) == 6:
        Xlog.write("K:")
    Xlog.write(move.uci()[2] + move.uci()[3])
    Xlog.write("\n")
    Xlog.close()
    return True

def writeMoveToYFile(move, board, player):
    Ylog = open("log_Y.txt", "a")
    Ylog.write(player)
    if board.piece_type_at(move.from_square) == 4:
        Ylog.write("R:")
    elif board.piece_type_at(move.from_square) == 2:
        Ylog.write("N:")
    elif board.piece_type_at(move.from_square) == 6:
        Ylog.write("K:")
    Ylog.write(move.uci()[2] + move.uci()[3])
    Ylog.write("\n")
    Ylog.close()
    return True

def play_game(white_move_func, black_move_func, display=False):
    total_Moves = 0
    b = chess.Bitboard('2n1k3/8/8/8/8/8/8/4K1NR w Kk - 0 1')
    if display:
        print(str(b) + '\n\n')
    move_functions = cycle([white_move_func, black_move_func])
    playerQuestion = input("Are you playing as X or Y: ")

    while not b.is_game_over():
        if playerQuestion == 'X':
            total_Moves = total_Moves + 1
            move_function = next(move_functions)
            m = move_function(b)
            writeMoveToXFile(m, b, 'X:')

            print("Total Moves: ", total_Moves)

            b.push(m)

            if display:
                print('\n' + str(m))
                print(str(b))
                weight_mod.weight(b)
                print('\n\n')

            input("Ready to Read Player Y's Move?")

            readMoveFromFileY(b)
            total_Moves = total_Moves + 1
            print("Total Moves: ", total_Moves)
            #moveToMake = input("What is Player Y's Move? ")

            #fromSpot = moveToMake[0] + moveToMake[1]
            #toSpot = moveToMake[2] + moveToMake[3]

            #fromSpotInt = toInt(fromSpot)
            #toSpotInt = toInt(toSpot)

            #m = Move(fromSpotInt, toSpotInt)

            #writeMoveToFileY(m, b, 'Y:')

            #print(m)

            #b.push(m)
        else:
            input("Ready to Read Player X's Move?")

            readMoveFromFileX(b)

            #moveToMake = input("What is Player X's Move? ")

            #fromSpot = moveToMake[0] + moveToMake[1]
            #toSpot = moveToMake[2] + moveToMake[3]

            #fromSpotInt = toInt(fromSpot)
            #toSpotInt = toInt(toSpot)

            #m = Move(fromSpotInt, toSpotInt)

            #writeMoveToXFile(m, b, 'X:')

            #print(m)

            #b.push(m)


            if display:
                print(str(b))
                weight_mod.weight(b)
                print('\n\n')

            move_function = next(move_functions)
            m = move_function(b)
            writeMoveToYFile(m, b, 'Y:')
            b.push(m)

        if display:
            print('\n' + str(m))
            print(str(b))
            weight_mod.weight(b)
            print('\n\n')

    if display:
        if b.is_stalemate():
            print("STALEMATE")
        elif b.is_insufficient_material():
            print("INSUFFICIENT MATERIAL")
        elif b.is_seventyfive_moves():
            print("75 MOVES DRAW")
        elif b.is_fivefold_repitition():
            print("5-FOLD REPITITION")
        elif b.is_checkmate():
            print("CHECKMATE")

    return b

def whites_turn(board):
    return board.turn == chess.WHITE


def white_wins(board):
    return board.is_checkmate() and whites_turn(board)


def generate_move_function(is_white, weight_func, steps_ahead):
    if is_white:
        weight = weight_func
    else:
        weight = lambda b: -weight_func(b)

    return adversarial_search(weight, possible_actions, step, steps_ahead)


def attackers(color, board, square):
    return len(board.attackers(color, square))


attacker_imbalance = white_minus_black(attackers)


def on_board(squares):
    return filter(lambda x: 0 <= x < 64, squares)


def adjacent_squares(square):

    adjs = [
        square - 8,
        square + 8,
    ]

    if chess.file_index(square) != 0:
        adjs.append(square - 9)
        adjs.append(square - 1)
        adjs.append(square + 7)
    if chess.file_index(square) != 7:
        adjs.append(square - 7)
        adjs.append(square + 1)
        adjs.append(square + 9)

    return on_board(adjs)


def sum_list(summands):
    return reduce(lambda x, y: x + y, summands, 0)


def get_piece_squares(board):
    for s in chess.SQUARES:
        p = board.piece_at(s)
        if not p is None:
            yield p, s


def get_pieces(board, on=chess.SQUARES):
    return filter(lambda x: not x is None, [board.piece_at(s) for s in on])


def pawn_protecting_squares(color, protected_square):
    if color == chess.WHITE:
        if chess.file_index(protected_square) == 0:
            return [protected_square - 7]
        elif chess.file_index(protected_square) == 7:
            return [protected_square - 9]
        else:
            return [protected_square - 9, protected_square - 7]
    else:
        if chess.file_index(protected_square) == 0:
            return [protected_square + 9]
        elif chess.file_index(protected_square) == 7:
            return [protected_square + 7]
        else:
            return [protected_square + 9, protected_square + 7]


def is_tie(board):
    return board.is_game_over() and not board.is_checkmate()


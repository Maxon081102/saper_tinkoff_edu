import random
import os
from save_game import download_game
from save_game import save_game
from alg_helper import do_help_turn


def start_game():
    print('Do you want to continue the game or start a new one?\nPlease, write Download or New')
    answer = input()
    if answer.lower() == 'download':
        print("write game's name")
        name_game = input()
        if name_game in os.listdir('../games'):
            return [name_game, download_game(name_game), 'd']

    elif answer.lower() == 'new':
        print("write game's name")
        name_game = input()
        data = {}
        return [name_game, data, 'n']
    else:
        print('error')
        start_game()


def check_bomb(arr, data):
    k = 0
    for elem in arr:
        if elem in data['bombs']:
            k += 1
    return k


"""
def write_number(X, Y, data):
    if X == 0:
        if Y == 0:
            k = check_bomb([[0, 1], [1, 0], [1, 1]], data)
            data['board'][X][Y] = f'{k}'
        elif Y == (data['y'] - 1):
            k = check_bomb([[1, Y], [0, Y - 1], [1, Y - 1]], data)
            data['board'][X][Y] = f'{k}'
        else:
            k = check_bomb([[0, Y + 1], [1, Y], [1, Y - 1], [1, Y + 1], [0, Y - 1]], data)
            data['board'][X][Y] = f'{k}'
    elif X == (data['x'] - 1):
        if Y == 0:
            k = check_bomb([[X, 1], [X, 0], [X, 1]], data)
            data['board'][X][Y] = f'{k}'
        elif Y == (data['y'] - 1):
            k = check_bomb([[X - 1, Y], [X, Y - 1], [X - 1, Y - 1]], data)
            data['board'][X][Y] = f'{k}'
        else:
            k = check_bomb([[X, Y + 1], [X - 1, Y], [X, Y - 1], [X - 1, Y + 1], [X - 1, Y - 1]], data)
            data['board'][X][Y] = f'{k}'
    else:
        if Y == 0:
            k = check_bomb([[X + 1, Y], [X - 1, Y], [X, Y + 1], [X + 1, Y + 1], [X - 1, Y + 1]], data)
            data['board'][X][Y] = f'{k}'
        elif Y == (data['y'] - 1):
            k = check_bomb([[X + 1, Y], [X - 1, Y], [X, Y - 1], [X + 1, Y - 1], [X - 1, Y - 1]], data)
            data['board'][X][Y] = f'{k}'
        else:
            k = check_bomb([[X + 1, Y], [X - 1, Y], [X, Y - 1], [X + 1, Y - 1], [X - 1, Y - 1],
                            [X, Y + 1], [X + 1, Y + 1], [X - 1, Y + 1]], data)
            data['board'][X][Y] = f'{k}'
"""


def gen_bombs(data):
    if len(data['bombs']) == data['number_of_bombs']:
        pass
    else:
        x, y = random.randint(0, data['x'] - 1), random.randint(0, data['y'] - 1)
        if [x, y] in data['bombs']:
            gen_bombs(data)
        else:
            data['bombs'].append([x, y])
            gen_bombs(data)


def do_big_board(data):
    gen_bombs(data)
    data['big_board'] = [[0 for i in range(data['x'] + 2)] for j in range(data['y'] + 2)]
    for i in range(1, data['y'] + 1):
        for j in range(1, data['x'] + 1):
            if [j - 1, i - 1] in data['bombs']:
                data['big_board'][i][j] = '@'
            else:
                data['big_board'][i][
                    j] = f'{check_bomb([[j - 1, i - 1], [j - 2, i - 1], [j - 1, i - 2], [j, i - 2], [j - 2, i - 2], [j - 1, i], [j, i], [j - 2, i], [j, i - 1]], data)}'


def turn(X, Y, action, data):
    if action.lower() == 'flag':
        data['board'][Y][X] = '!'
        return 1
    elif action.lower() == 'open':
        if [X, Y] in data['bombs']:
            return 0
        else:
            if data['big_board'][Y + 1][X + 1] == '0':
                open_null(X, Y, data)
                data['open_points'].append([X, Y])
                return 1
            else:
                data['board'][Y][X] = data['big_board'][Y + 1][X + 1]
                data['open_points'].append([X, Y])
                return 1
    elif action.lower() == 'help':
        X, Y = do_help_turn(data)
        if [X, Y] in data['bombs']:
            return 0
        else:
            data['board'][Y][X] = data['big_board'][Y + 1][X + 1]
            data['open_points'].append([X, Y])
            return 1


def check_game(data):
    open_points = 0
    for i in range(data['y']):
        for j in range(data['x']):
            if data['board'][i][j].isdecimal():
                open_points += 1
    if open_points + len(data['bombs']) == data['y'] * data['x']:
        return True


def open_null(X, Y, data):
    queue = [[X, Y]]
    while queue:
        cur_point = queue.pop()
        data['board'][cur_point[1]][cur_point[0]] = data['big_board'][cur_point[1] + 1][cur_point[0] + 1]
        if data['big_board'][cur_point[1] + 1][cur_point[0] + 1] == '0':
            for point in [[cur_point[0], cur_point[1] + 1], [cur_point[0], cur_point[1] - 1],
                          [cur_point[0] + 1, cur_point[1]], [cur_point[0] - 1, cur_point[1]]]:
                if 0 <= point[0] < data[
                    'x'] and 0 <= point[1] < data['y']:
                    if data['board'][point[1]][point[0]] == '#' and point not in queue:
                        queue.append(point)


"""
class Game:
    def __init__(self, mode, x=5, y=5, number_of_bombs=False):
        self.x = x
        self.y = y
        self.number_of_bombs = number_of_bombs
        if number_of_bombs is False:
            self.number_of_bombs = random.randint(2, 5)
        self.mode = mode
        self.board = []
        self.flags = []
        self.bombs = []
        self.open_fields = []
        self.turn = 0

    def mode(self):
        pass

    def make_board(self):
        for i in range(self.y):
            self.board.append([])
            for j in range(self.x):
                self.board[i].append('#')

    def show_board(self):
        for i in range(self.y):
            print()
            for j in range(self.x):
                print(self.board[i][j], end=' ')

    def turn(self, x, y, action):
        pass

"""


def show_board(data):
    for i in range(data['y']):
        print()
        for j in range(data['x']):
            print(data['board'][i][j], end=' ')


def show_board2(data):
    for i in range(data['y'] + 2):
        print()
        for j in range(data['x'] + 2):
            print(data['big_board'][i][j], end=' ')


if __name__ == "__main__":
    while True:
        game = start_game()
        if game[2] == 'n':
            print("write mode game: a or b")
            mode = input()
            if mode.lower() == 'a':
                game[1]['x'] = 5
                game[1]['y'] = 5
                game[1]['number_of_bombs'] = random.randint(2, 5)
                game[1]['bombs'] = []
                game[1]['board'] = [['#' for i in range(5)] for j in range(5)]
                game[1]['turn'] = 1
                game[1]['open_points'] = []
            elif mode.lower() == 'b':
                print("write x y number_of_bombs like this ( first x,second y,third number_of_bombs): 4 3 2")
                _ = list(map(int, input().split()))
                game[1]['x'] = _[0]
                game[1]['y'] = _[1]
                game[1]['number_of_bombs'] = _[2]
                game[1]['bombs'] = []
                game[1]['board'] = [['#' for i in range(_[0])] for j in range(_[1])]
                game[1]['turn'] = 1
                game[1]['open_points'] = []
            do_big_board(game[1])
        print('Play has started!')
        session_of_game = True
        while session_of_game:
            ask = input().split()
            X = int(ask[0])
            Y = int(ask[1])
            action = ask[2]
            continue_ = turn(X, Y, action, game[1])
            if not continue_:
                session_of_game = False
                print('Я тебя переиграл и уничтожил')
            elif check_game(game[1]):
                print('You Win!!!')
                session_of_game = False
            else:
                show_board(game[1])
                print()
                show_board2(game[1])
                print()
                save_game(game[0], game[1])

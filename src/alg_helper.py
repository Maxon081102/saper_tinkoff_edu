import random


def do_sets(data):
    bomb_sets = []
    for i in range(data['y']):
        for j in range(data['x']):
            if data['board'][i][j].isdecimal() and data['board'][i][j] != '0':
                cur_point_set = [set(), int(data['board'][i][j])]
                for point in [[j + 1, i], [j - 1, i], [j, i + 1], [j, i - 1], [j + 1, i + 1], [j - 1, i - 1],
                              [j + 1, i - 1], [j - 1, i + 1]]:
                    if 0 <= point[0] < data[
                        'x'] and 0 <= point[1] < data['y']:
                        if data['board'][point[1]][point[0]] == '#':
                            cur_point_set[0].add(data['x'] * point[1] + point[0] + 1)
                bomb_sets.append(cur_point_set)
    return bomb_sets


def mix_groups(bomb_sets, data):
    amount_of_doing_nothing = 0
    while amount_of_doing_nothing < data['x'] * data['y']:
        i = 0
        j = 0
        while i < len(bomb_sets):
            while j < len(bomb_sets):
                if i == j:
                    j += 1
                    amount_of_doing_nothing += 1
                else:
                    if bomb_sets[i][0] == bomb_sets[j][0] and bomb_sets[i][1] == bomb_sets[j][1]:
                        bomb_sets.pop(j)
                        amount_of_doing_nothing = 0
                    elif bomb_sets[i][0].issubset(bomb_sets[j][0]):
                        bomb_sets[j][0] -= bomb_sets[i][0]
                        bomb_sets[j][1] -= bomb_sets[i][1]
                        amount_of_doing_nothing = 0
                    elif bomb_sets[j][0].issubset(bomb_sets[i][0]):
                        bomb_sets[i][0] -= bomb_sets[j][0]
                        bomb_sets[i][1] -= bomb_sets[j][1]
                        amount_of_doing_nothing = 0
                    elif bomb_sets[i][0] & bomb_sets[j][0] and bomb_sets[i][1] != bomb_sets[j][1]:
                        new_set = bomb_sets[i][0] & bomb_sets[j][0]
                        if bomb_sets[i][1] > bomb_sets[j][1]:
                            boms_in_new_set = bomb_sets[i][1]
                            bomb_sets[j][0] -= new_set
                            boms_in_new_set -= len(bomb_sets[j][0])
                        else:
                            boms_in_new_set = bomb_sets[j][1]
                            bomb_sets[i][0] -= new_set
                            boms_in_new_set -= len(bomb_sets[i][0])
                        if boms_in_new_set != min(bomb_sets[i][1], bomb_sets[j][1]):
                            bomb_sets.append([new_set, boms_in_new_set])
                        else:
                            bomb_sets[i][0] -= new_set
                            bomb_sets[j][0] -= new_set
                            bomb_sets[i][1] -= boms_in_new_set
                            bomb_sets[j][1] -= boms_in_new_set
                            bomb_sets.append([new_set, boms_in_new_set])
                        amount_of_doing_nothing = 0
                    else:
                        amount_of_doing_nothing += 1
                    j += 1
            i += 1
    return bomb_sets


def do_help_turn(data, turn):
    if turn == 1:
        return random.randint(0, data['x'] - 1), random.randint(0, data['y'] - 1)
    bomb_sets = mix_groups(do_sets(data), data)
    for elem in bomb_sets:
        if elem[1] == 0:
            return list(elem[0])[0] % data['x'] - 1, list(elem[0])[0] // data['x']
    close_point = []
    for i in range(data['y']):
        for j in range(data['x']):
            if data['board'][i][j] == '#':
                close_point.append([j, i])
    point = random.choice(close_point)
    return point[0], point[1]

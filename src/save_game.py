import pickle


def download_game(name):
    with open(f'../games/{name}', 'rb') as f:
        game = pickle.load(f)
    return game


def save_game(name, data):
    with open(f'../games/{name}', 'wb') as f:
        pickle.dump(data, f)

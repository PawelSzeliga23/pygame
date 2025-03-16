class Saver:
    def __init__(self, path):
        self.path = path

    def save(self, score, name):
        if name == '':
            return None
        if score == 0:
            return None
        with open(self.path, 'a') as f:
            f.write(f'{name}: {score}\n')

    def load(self):
        with open(self.path, 'r') as f:
            return f.readlines()

import random

class Player():
    def __init__(self, id):
        self.id = id
        self.score = 0
        self.hand = Hand()
        self.position = Position()

class Board():
    def __init__(self):
        self.grid_length = 7
        self.n_players = 2
        self.num_squares = self.grid_length * self.grid_length
        self.grid_shape = (self.grid_shape, self.grid_shape)
        self.n_growths = 7*7*8
        self.n_jumps = 7*7*16
        self.n_actions = self.n_growths + self.n_jumps
        self.growths = [(-1,-1), (-1,0), (-1, 1), (0,-1), (0, 1), (1,-1), (1,0), (1, 1)]
        self.jumps = [(-2,x) for x in (-2,-1,0,1,2)] + [(-1,-2),(-1,2), (0,-2),(0,2), (1,-2),(1,2)] + [(2,x) for x in (-2,-1,0,1,2)]

    def decode_move(self, n):
        if n < self.n_growths:
            coords, diff = divmod(n, 8)
            dy,dx = self.growths[diff]
        else:
            coords, diff = divmod(n - self.n_growths, 16)
            dy,dx = self.jumps[diff]
        y,x = divmod(coords, self.grid_length)
        return x,y,x+dx,y+dy

    def encode_move(self, x1,y1,x2,y2):
        kind = 'growth' if abs(x2-x1) <= 1 and abs(y2-y1) <= 1 else 'jump'
        dx = x2 - x1
        dy = y2 - y1
        if abs(dx) > 2 or abs(dy) > 2:
            raise Exception('Invalid move: cannot jump more than 2 spaces')
        elif abs(dx) == 0 and abs(dy) == 0:
            raise Exception('Invalid move: start and end space are the same')
        elif abs(dx) <= 1 and abs(dy) <= 1:   # GROWTH
            return (y1 * 7 + x1) * 8 + self.growths.index((dy,dx))
        else:    # JUMP
            return self.n_growths + (y1 * 7 + x1) * 16 + self.jumps.index((dy,dx))

class Card():
    def __init__(self, id, order, name):
        self.id = id
        self.order = order
        self.name = name

class Deck():
    def __init__(self, contents):
        self.contents = contents
        self.create()

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self, n):
        drawn = []
        for x in range(n):
            drawn.append(self.cards.pop())
        return drawn

    def add(self, cards):
        for card in cards:
            self.cards.append(card)

    def create(self):
        self.cards = []

        card_id = 0
        for order, x in enumerate(self.contents):
            x['info']['order'] = order
            for i in range(x['count']):
                x['info']['id'] = card_id
                self.add([x['card'](**x['info'])])
                card_id += 1

        self.shuffle()

    def size(self):
        return len(self.cards)


class Hand():
    def __init__(self):
        self.cards = []

    def add(self, cards):
        for card in cards:
            self.cards.append(card)

    def size(self):
        return len(self.cards)

    def pick(self, name):
        for i, c in enumerate(self.cards):
            if c.name == name:
                self.cards.pop(i)
                return c


class Discard():
    def __init__(self):
        self.cards = []

    def add(self, cards):
        for card in cards:
            self.cards.append(card)

    def size(self):
        return len(self.cards)

class Position():
    def __init__(self):
        self.cards = []

    def add(self, cards):
        for card in cards:
            self.cards.append(card)

    def size(self):
        return len(self.cards)

    def pick(self, name):
        for i, c in enumerate(self.cards):
            if c.name == name:
                self.cards.pop(i)
                return c

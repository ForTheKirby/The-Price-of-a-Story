class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.value = self.get_card_value()

    def __str__(self):
        if self.rank == 'Joker':
            return '🃏 Joker'
        return f"{self.rank}{self.suit}"

    def get_card_value(self):
        if self.rank in ['Jack', 'Queen', 'King']:
            return 10
        elif self.rank == 'Ace':
            return 1
        elif self.rank == 'Joker':
            return 0
        return int(self.rank)

    def is_numeric(self):
        return self.rank.isdigit() or self.rank == 'Ace'

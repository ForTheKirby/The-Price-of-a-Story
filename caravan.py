class Caravan:
    def __init__(self):
        self.cards = []
        self.direction = None
        self.suit = None

    def __str__(self):
        return " ".join(str(card) for card in self.cards)

    def total(self):
        total = 0
        multipliers = {}
        for i, card in enumerate(self.cards):
            if card.rank == 'King':
                if i > 0:
                    prev = self.cards[i - 1]
                    if prev.is_numeric():
                        multipliers[prev] = multipliers.get(prev, 1) * 2
            elif card.is_numeric():
                mult = multipliers.get(card, 1)
                total += card.value * mult
        return total

    def add_card(self, card):
        if not self.cards:
            if card.is_numeric():
                self.cards.append(card)
                self.suit = card.suit
                return True
            return False

        if card.rank in ['Jack', 'Queen', 'King', 'Joker']:
            self.cards.append(card)
            return True

        last_card = next((c for c in reversed(self.cards) if c.is_numeric()), None)
        if not last_card:
            return False

        if self.direction is None:
            if card.suit != self.suit or card.value == last_card.value:
                return False
            self.direction = 'up' if card.value > last_card.value else 'down'
            self.cards.append(card)
            return True

        if card.suit == self.suit or \
           (self.direction == 'up' and card.value > last_card.value) or \
           (self.direction == 'down' and card.value < last_card.value):
            if card.value != last_card.value:
                self.cards.append(card)
                return True

        return False

    def remove_card_at(self, index):
        if 0 <= index < len(self.cards):
            del self.cards[index]

    def reset(self):
        self.cards = []
        self.direction = None
        self.suit = None

from caravan import Caravan

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.caravans = [Caravan(), Caravan(), Caravan()]
        self.discard_pile = []

    def draw_hand(self, deck, count=5):
        while len(self.hand) < count and deck:
            self.hand.append(deck.pop())

    def start_caravans(self, deck):
        for i in range(3):
            for j, card in enumerate(self.hand):
                if card.is_numeric():
                    self.caravans[i].add_card(card)
                    self.hand.pop(j)
                    break
        self.draw_hand(deck)

    def play_card_to_caravan(self, card_index, caravan_index, opponent=False, opponent_player=None):
        card = self.hand[card_index]
        if card.rank in ['Jack', 'Queen', 'King', 'Joker'] and opponent:
            return self.play_special_card(card_index, caravan_index, opponent_player)

        target_caravan = self.caravans[caravan_index]
        if target_caravan.add_card(card):
            self.hand.pop(card_index)
            return True
        return False

    def discard_card(self, card_index):
        card = self.hand.pop(card_index)
        self.discard_pile.append(card)

    def reset_caravan(self, index):
        self.caravans[index].reset()

    def get_total_score(self):
        return sum(1 for c in self.caravans if 21 <= c.total() <= 26)

    def play_special_card(self, card_index, caravan_index, opponent_player):
        card = self.hand[card_index]
        target = opponent_player.caravans[caravan_index]

        if not target.cards:
            return False

        if card.rank == 'Jack':
            # Remove last numeric card and attached face cards
            for i in range(len(target.cards) - 1, -1, -1):
                if target.cards[i].is_numeric():
                    target.cards = target.cards[:i]
                    break
        elif card.rank == 'Queen':
            target.direction = 'up' if target.direction == 'down' else 'down'
            target.suit = target.cards[-1].suit
            target.cards.append(card)
        elif card.rank == 'King':
            target.cards.append(card)
        elif card.rank == 'Joker':
            # Simplified logic for now
            target.cards.append(card)
        else:
            return False

        self.hand.pop(card_index)
        return True

import os
import random
from card import Card
from player import Player

suits = ['♠', '♥', '♦', '♣']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def create_deck():
    deck = [Card(rank, suit) for suit in suits for rank in ranks]
    deck += [Card('Joker', '') for _ in range(2)]
    random.shuffle(deck)
    return deck

def display_caravans(player, opponent=False):
    print(f"\n{player.name}'s Caravans:")
    for i, c in enumerate(player.caravans):
        print(f"  Caravan {i+1}: [{c}]  Total: {c.total()}")

def display_hand(player):
    print(f"\n{player.name}'s Hand:")
    for i, card in enumerate(player.hand):
        print(f"  {i+1}. {card}")

def play_turn(player, opponent, deck):
    while True:
        clear()
        print(f"=== {player.name}'s Turn ===")
        display_caravans(player)
        display_caravans(opponent)
        display_hand(player)

        print("\nOptions:")
        print("1. Play card on your caravan")
        print("2. Play special card on opponent caravan")
        print("3. Discard a card")
        print("4. Discard one of your caravans")
        choice = input("Choose an action (1-4): ").strip()

        try:
            if choice == '1':
                ci = int(input("Choose card index: ")) - 1
                cv = int(input("Choose your caravan (1-3): ")) - 1
                if player.play_card_to_caravan(ci, cv):
                    break
                else:
                    input("Invalid move. Press Enter to continue.")
            elif choice == '2':
                ci = int(input("Choose card index: ")) - 1
                cv = int(input("Choose opponent caravan (1-3): ")) - 1
                if player.play_card_to_caravan(ci, cv, opponent=True, opponent_player=opponent):
                    break
                else:
                    input("Invalid special move. Press Enter to continue.")
            elif choice == '3':
                ci = int(input("Choose card index to discard: ")) - 1
                player.discard_card(ci)
                break
            elif choice == '4':
                cv = int(input("Choose caravan to discard (1-3): ")) - 1
                player.reset_caravan(cv)
                break
        except:
            input("Invalid input. Press Enter to continue.")

    player.draw_hand(deck)

def check_winner(player, ai):
    if player.get_total_score() >= 2:
        return player.name
    elif ai.get_total_score() >= 2:
        return ai.name
    return None

def ai_turn(ai, player, deck):
    # Super simple AI for now
    for i, card in enumerate(ai.hand):
        for c in range(3):
            if card.rank in ['Jack', 'Queen', 'King', 'Joker']:
                if ai.play_card_to_caravan(i, c, opponent=True, opponent_player=player):
                    ai.draw_hand(deck)
                    return
            if ai.play_card_to_caravan(i, c):
                ai.draw_hand(deck)
                return
    ai.discard_card(0)
    ai.draw_hand(deck)

def play_game():
    deck = create_deck()
    player = Player("You")
    ai = Player("AI")

    for _ in range(8):
        player.draw_hand(deck)
        ai.draw_hand(deck)

    player.start_caravans(deck)
    ai.start_caravans(deck)

    while True:
        play_turn(player, ai, deck)
        winner = check_winner(player, ai)
        if winner:
            break
        ai_turn(ai, player, deck)
        winner = check_winner(player, ai)
        if winner:
            break

    clear()
    display_caravans(player)
    display_caravans(ai)
    print(f"\n🏆 Game Over! {winner} wins! 🏆")

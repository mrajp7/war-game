from deck import Deck, Pile, Card
from logzero import logger
from enum import Enum

logger.setLevel("DEBUG")

class GameStatus(Enum):
    Player1Wins = 0
    Player2Wins = 1
    Tie = 2

class WarGame:
    def __init__(self, deck:Deck, shuffle_pile:bool = True):
        self.deck = deck
        self.shuffle_pile = shuffle_pile
        self.player1 = Pile(self.deck.deck_id, "Player1")
        self.player2 = Pile(self.deck.deck_id, "Player2")
        self.round_num = 0
        self.status = GameStatus.Tie
        self.round_status = GameStatus.Tie
        self.table_cards = []

    def deal_cards(self):
        # while self.deck.remaining_cards > 0:
        #     self.player1.add_cards(self.deck.draw())
        #     self.player2.add_cards(self.deck.draw())
        # ! Assumption / Consideration: To reduce the # of calls drawing half the cards at once
        count = self.deck.remaining_cards
        self.player1.add_cards(self.deck.draw(num_cards=round(count/2)))
        self.player2.add_cards(self.deck.draw(num_cards=int(count/2)))
        logger.info("Card has been dealt")

    def play_a_turn(self):
        if self.round_num == 0:
                logger.info("Starting War game...")
        logger.info(f"Round {self.round_num + 1}:")
        if self.shuffle_pile and self.round_num != 0 and self.round_num % 10 == 0:
                logger.debug("Shuffling Players card every 10 turns")
                self.player1.shuffle_pile()
                self.player2.shuffle_pile()
        logger.debug(f"Player1 Card count - {self.player1.remaining_cards}")
        logger.debug(f"Player2 Card count - {self.player2.remaining_cards}")

        p1_card = self.player1.draw()[0]
        p2_card = self.player2.draw()[0]
        self.table_cards.extend([p1_card, p2_card])
        logger.debug(f"Cards in table - {len(self.table_cards)}")
        logger.info(f"Player 1 plays: {p1_card.value} of {p1_card.suit}")
        logger.info(f"Player 2 plays: {p2_card.value} of {p2_card.suit}")

        if get_card_value(p1_card) > get_card_value(p2_card):
            logger.info("Player 1 wins the round!")
            self.player1.add_cards(self.table_cards)
            self.table_cards.clear()
            self.round_status = GameStatus.Player1Wins
        elif get_card_value(p2_card) > get_card_value(p1_card):
            logger.info("Player 2 wins the round!")
            self.player2.add_cards(self.table_cards)
            self.table_cards.clear()
            self.round_status = GameStatus.Player2Wins
        elif get_card_value(p1_card) == get_card_value(p2_card):
            logger.info("Tie! Its a war")
            self.round_status = GameStatus.Tie
            # continue.
            self.table_cards.append(self.player1.draw()[0])
            self.table_cards.append(self.player2.draw()[0])

        self.round_num += 1

    def check_game_status(self):
        if self.player1.remaining_cards > self.player2.remaining_cards:
            logger.info("Player 1 wins the game!")
            self.status = GameStatus.Player1Wins
        elif self.player1.remaining_cards < self.player2.remaining_cards:
            logger.info("Player 2 wins the game!")
            self.status = GameStatus.Player2Wins
        else:
            logger.info("It's a tie!")
            self.status = GameStatus.Tie
        
    def play_game(self, max_turns:int = 5000):

        while self.player1.remaining_cards > 0 and self.player2.remaining_cards > 0 \
            and self.round_num < max_turns:
            self.play_a_turn()

        self.check_game_status()

def get_card_value(card:Card):
    value = card.value
    if value == 'ACE':
        return 14
    elif value == 'KING':
        return 13
    elif value == 'QUEEN':
        return 12
    elif value == 'JACK':
        return 11
    else:
        return int(value)
    
if __name__ == "__main__":
    deck = Deck()
    deck.shuffled_deck()
    game = WarGame(deck)
    game.deal_cards()
    game.play_game(5000)

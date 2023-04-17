from collections import namedtuple
from api import RequestMethod as Method
from api import APIRequest

# region Deck API Constants

DeckEndpoint = namedtuple('Deck',['method','endpoint'])
base_url = "https://deckofcardsapi.com/api/deck"

s_deck = DeckEndpoint(Method.GET, "/new/shuffle")
new_deck = DeckEndpoint(Method.GET, "/new")
shuf = DeckEndpoint(Method.GET, "/{deck_id}/shuffle")
draw = DeckEndpoint(Method.GET, "/{deck_id}/draw")
add_to_pile = DeckEndpoint(Method.GET, "/{deck_id}/pile/{pile}/add")
shuf_pile = DeckEndpoint(Method.GET, "/{deck_id}/pile/{pile}/shuffle")
list_pile = DeckEndpoint(Method.GET, "/{deck_id}/pile/{pile}/list")
draw_pile_cards = DeckEndpoint(Method.GET, "/{deck_id}/pile/{pile}/draw")
draw_pile_top = DeckEndpoint(Method.GET, "/{deck_id}/pile/{pile}/draw")
draw_pile_bottom = DeckEndpoint(Method.GET, "/{deck_id}/pile/{pile}/draw/bottom")
draw_pile_random = DeckEndpoint(Method.GET, "/{deck_id}/pile/{pile}/draw/random")

# endregion

def parse_cards(cards:list):
    return [ Card(card['code'],card['value'],card['suit']) 
                                        for card in cards ]

class Card:
    """_summary_
    A class that defines a card property
    """
    def __init__(self, code, value, suit) -> None:
        self.code = code
        self.value = value
        self.suit = suit

    def __str__(self) -> str:
        return f"{self.code}"

class Deck:
    """
    Represents properties of a Deck
    """
    def __init__(self):
        self.deck_id = None
        self.remaining_cards = None

    def new_deck(self):
        data = APIRequest.APIRequestBuilder(base_url)\
            .build()\
            .send_request(new_deck.method, new_deck.endpoint)\
            .get_response_json()
        self.deck_id = data['deck_id']
        self.remaining_cards = data['remaining']

    def shuffled_deck(self, count=1):
        data = APIRequest.APIRequestBuilder(base_url)\
            .add_param('deck_count', count)\
            .build()\
            .send_request(s_deck.method, s_deck.endpoint)\
            .get_response_json()
        self.deck_id = data['deck_id']
        self.remaining_cards = data['remaining']
    
    def partial_deck(self, card_codes:list):
        data = APIRequest.APIRequestBuilder(base_url)\
            .add_param('cards', ",".join(card_codes))\
            .build()\
            .send_request(new_deck.method, new_deck.endpoint)\
            .get_response_json()
        self.deck_id = data['deck_id']
        self.remaining_cards = data['remaining']

    def partial_shuffled_deck(self, card_codes:list):
        data = APIRequest.APIRequestBuilder(base_url)\
            .add_param('cards', ",".join(card_codes))\
            .build()\
            .send_request(s_deck.method, s_deck.endpoint)\
            .get_response_json()
        self.deck_id = data['deck_id']
        self.remaining_cards = data['remaining']

    def shuffle(self, remaining:bool = True):
        data = APIRequest.APIRequestBuilder(base_url)\
            .add_param('remaining', remaining)\
            .build()\
            .send_request(shuf.method, shuf.endpoint.format(deck_id=self.deck_id))\
            .get_response_json()
        self.remaining_cards = data['remaining']

    def draw(self, num_cards=1):
        if num_cards > self.remaining_cards:
            raise ValueError("Not enough cards remaining in deck.")
        data = APIRequest.APIRequestBuilder(base_url)\
            .add_param('count', num_cards)\
            .build()\
            .send_request(draw.method, draw.endpoint.format(deck_id=self.deck_id))\
            .get_response_json()
        self.remaining_cards = data['remaining']
        cards = data['cards']
        return parse_cards(cards)
    
class Pile:
    """_summary_
    Represents a Pile from the Deck
    """
    def __init__(self, deck_id:str, pile_name:str):
        self.deck_id = deck_id
        self.pile_name = pile_name
        self.remaining_cards = 0

    def add_cards(self, cards:list):
        card_codes = [card.code for card in cards]
        data = APIRequest.APIRequestBuilder(base_url)\
                .add_param('cards', ",".join(card_codes))\
                .build()\
                .send_request(add_to_pile.method, 
                    add_to_pile.endpoint.format(deck_id=self.deck_id,pile=self.pile_name))\
                .get_response_json()
        self.remaining_cards = data["piles"][self.pile_name]["remaining"]
    
    def list_cards(self):
        data = APIRequest.APIRequestBuilder(base_url)\
                .build()\
                .send_request(list_pile.method, 
                    list_pile.endpoint.format(deck_id=self.deck_id,pile=self.pile_name))\
                .get_response_json()
        cards = data["piles"][self.pile_name]["cards"]
        return parse_cards(cards)

    def shuffle_pile(self):
        data = APIRequest.APIRequestBuilder(base_url)\
                .build()\
                .send_request(shuf_pile.method, 
                    shuf_pile.endpoint.format(deck_id=self.deck_id,pile=self.pile_name))\
                .get_response_json()
        self.remaining_cards = data["piles"][self.pile_name]["remaining"]

    def draw(self, num_cards=1):
        if num_cards > self.remaining_cards:
            raise ValueError("Not enough cards remaining in pile.")
        data = APIRequest.APIRequestBuilder(base_url)\
            .add_param('count', num_cards)\
            .build()\
            .send_request(draw_pile_bottom.method, 
                draw_pile_bottom.endpoint.format(deck_id=self.deck_id,pile=self.pile_name))\
            .get_response_json()
        self.remaining_cards = data["piles"][self.pile_name]["remaining"]
        cards = data['cards']
        return parse_cards(cards)
    
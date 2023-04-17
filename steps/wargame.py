from behave import given, when, then
from deck import Deck
from war_game import WarGame, GameStatus

game_status = {
    "player1" : GameStatus.Player1Wins,
    "player2" : GameStatus.Player2Wins,
    "tie" : GameStatus.Tie
}

def get_game_status(status):
    if status in game_status.keys():
        return game_status[status]
    return GameStatus.Tie

@given(u'that a {d_type} deck of cards is provided')
def step_impl(context, d_type):
    deck = Deck()
    shuffle = True
    if d_type.lower() == "new":
        deck.new_deck()
        shuffle = False
    else:
        deck.shuffled_deck()
    context.deck = deck
    context.wargame = WarGame(context.deck, shuffle)

@given(u'the deck is divided into 2')
def step_impl(context):
    context.wargame.deal_cards()

@given(u'that a partial deck of cards "{cards}" is provided')
def step_impl(context, cards):
    deck = Deck()
    cards = cards.split(",")
    deck.partial_deck(cards)
    context.deck = deck
    context.wargame = WarGame(context.deck, False)

@then(u'there will be a war in the first round')
def step_impl(context):
    # On turn 1 war, expect to have a war and no
    assert len(context.wargame.table_cards) == 4
    assert context.wargame.round_status == GameStatus.Tie

@then(u'the winner will be {player} within {x} turns')
def step_impl(context, player, x):
    context.wargame.play_game()
    assert context.wargame.round_num < int(x)
    assert context.wargame.status == get_game_status(player)

@when(u'the game of war is played')
def step_impl(context):
    context.wargame.play_game()

@when(u'a single round is played')
def step_impl(context):
    context.wargame.play_a_turn()

@then(u'there will be a winner within {x} turns')
def step_impl(context, x):
    assert context.wargame.round_num < int(x)
    assert context.wargame.status == GameStatus.Player1Wins or \
        context.wargame.status == GameStatus.Player2Wins
    
@then(u'the cards on table to be 52')
def step_impl(context):
    assert len(context.wargame.table_cards) == 52
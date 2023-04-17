# Prerequisite
 - python3 and pip3 to be installed
 - Install the packages by running the below command
 >$ pip3 install -r requirements.txt

# Run tests
 - Run the following commands
 >$ behave wargame.feature
 - To include a html report run the following command
 >$ behave -f html -o report.html wargame.feature

# Assumptions or Considerations
- The War game uses a deck in 3 possible ways
    - Shuffled Deck of cards
    - New Deck of cards
    - Partial Deck
- The War game uses Piles from a deck as Players (Total 2 players can play the game)
- The Deck and Pile are representation of entities that in turns uses Deck of Card APIs
- To increase the possibilities of winning, on every 10 turns each players cards are shuffled.
- While dealing the card for both the players, instead of drawing one by one,
    - Player1.add_cards(deck.remaining_cards / 2)
    - Player2.add_cards(deck.remaining_cards / 2)
    ,i.e., half of the deck is added at once for each player, to avoid back to back API calls
- The player cards are drawn from Bottom on the Pile (Since winning cards are added to the top)
- Max turn the game will continue is 5000.

# Sample Runs:

Game Settings: Deck of 52 Shuffled Cards
- Run 1: [Round 84] Player 2 wins the game
- Run 2: [Round 244] Player 1 wins the game
- Run 3: [Round 346] Player 1 wins the game
- Run 4: [Round 138] Player 1 wins the game
- Run 5: [Round 367] Player 2 wins the game

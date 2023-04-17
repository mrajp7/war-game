Feature: Game of war
    This feature demonstrates the functionalitiy of Game of war using Deck of Cards API

Scenario: A winner is found within 100 turns
Given that a standard deck of cards is provided
And the deck is divided into 2
When the game of war is played
Then there will be a winner within 100 turns

Scenario: Validate the war scenario works as expected
Given that a partial deck of cards "2S,9S,5S,2D,4D,9D" is provided
And the deck is divided into 2
When a single round is played
Then there will be a war in the first round
And the winner will be player2 within 3 turns

Scenario: Validate there is a series of war scenario works as expected
Given that a new deck of cards is provided
And the deck is divided into 2
When the game of war is played
Then the winner will be tie within 14 turns
And the cards on table to be 52
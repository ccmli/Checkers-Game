# Checkers Game
This program implements a two-player Checkers game, where each player tries to capture all of the opponent's pieces or block them so that they cannot make any more moves. The game is played on an 8x8 checkerboard.

## Classes
### Checkers
Represents the Checkers game as played. It contains information about the board and the players. The board is initialized when the Checkers object is created. It has methods for creating players, playing the game, getting checker details, printing the board, and determining the game winner.

### Player
Represents a player in the game. It is initialized with the player's name and chosen piece color. Each player has a list of pieces, and methods to get the number of king pieces, triple king pieces, and captured opponent pieces.

### Board
Represents the checkerboard with 8 rows and 8 columns. It keeps track of the pieces on the board and provides methods to add and remove pieces.

### Square
Represents a square on the checkerboard. It can hold a checker piece.

### Piece
Represents a checker piece. It has properties like owner, color, location, and whether it is a king or triple king. It also provides methods to promote the piece to king or triple king.

## Exceptions
The program defines three custom exceptions:

OutofTurn: Raised if a player attempts to move a piece out of turn.
InvalidSquare: Raised if a player does not own the checker present in the square_location or if the square_location does not exist on the board.
InvalidPlayer: Raised if the player name is not valid.

## How to Play
Create a new instance of the Checkers class to start the game.
Use the create_player() method to create players, specifying their names and piece colors ("Black" or "White").
Play the game using the play_game() method, providing the player name, starting square location, and destination square location.
The game will handle the moves, capturing pieces, and determining the winner.
Use the print_board() method to display the current state of the board.
To check if the game has ended and get the winner, use the game_winner() method.
Remember to handle the custom exceptions (OutofTurn, InvalidSquare, InvalidPlayer) appropriately to ensure smooth gameplay.

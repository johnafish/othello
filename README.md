# othello
## A simple game of othello with an AI opponent.

###Description
Othello is a game that is played in a player vs. computer format. It is a two player game with each player having a colour (typically black and white), and the goal of the game is to finish with more tiles of your colour on the board than the tiles of your opponents colour.

The game takes place on an 8x8 grid with a middle 2x2 square filled with pieces of alternating colour. The players take turns placing tiles of their respective colours. If placing the tile creates a continuous line of tiles with their colour at the beginning and end of the line, all the tiles in the line “flip” to become their colour.

For a move to be valid it must create one of the aforementioned lines. If there are no valid moves, you must pass your turn to your opponent.
The game is completed once both players cannot move, and the player with more tiles of their colour on the board wins.

###Instructions to Play
To play Othello, run the file _othello.py_ in IDLE for Python 3.x, and press F5 to run the program. You can also run it in any Python 3.x interpreter.

You will be presented with an 8x8 grid on the screen with a 2x2 square of alternating tiles in the middle as described above. There will be a scoreboard in the bottom section of the screen to keep track of your score (how many tiles of your colour) and to indicate whose turn it is.

When it is your turn, you may move your mouse over the board and the tile under it will turn either red or green, depending on the validity of your move. If you are positioned for a valid move, clicking will place a tile and flip the tiles required.

If you wish to restart or create a new game, you may press the “Restart” button in the bottom section of the screen. To quit, you may press the “Quit” button beside the “Restart” button.

###TO DO:
- Better AI (minimax with alpha beta pruning is end-goal)
- Player turn indicator
- Win/loss indicator
- Restart/Quit GUI
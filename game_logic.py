"""
Game Logic module for Tic-Tac-Toe.

This module encapsulates the core rules of Tic-Tac-Toe:
- Board representation (9-element list).
- Turn management ('X' always starts, turns alternate).
- Move validation (preventing moves out of bounds or on occupied squares).
- Win condition detection across rows, columns, and diagonals.
- Draw detection when all squares are filled without a winner.
"""


class TicTacToeGame:
    """
    Manages the state and rules for a single match of Tic-Tac-Toe.
    
    The 3x3 board is represented as a 1D list of length 9:
        0 | 1 | 2
       ---+---+---
        3 | 4 | 5
       ---+---+---
        6 | 7 | 8
    """

    # All 8 possible straight lines that yield a win in Tic-Tac-Toe:
    # 3 Horizontal rows, 3 Vertical columns, 2 Diagonals.
    WINNING_COMBINATIONS = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]              # Diagonals
    ]

    def __init__(self):
        """Initialize a fresh game state."""
        self.board = [""] * 9           # 9 empty squares
        self.current_player = "X"       # 'X' always makes the first move
        self.winner = None              # Will hold 'X' or 'O' when a player wins
        self.winning_combo = []         # Holds the 3 indices of the winning line
        self.is_draw = False            # True when board is full and no winner
        self.move_count = 0             # Number of moves made in current round

    def reset(self):
        """Reset the board to start a new round."""
        self.board = [""] * 9
        self.current_player = "X"
        self.winner = None
        self.winning_combo = []
        self.is_draw = False
        self.move_count = 0

    def is_valid_move(self, position):
        """
        Check if a move to a given board position is legal.
        
        A move is valid if and only if:
        1. Position is an integer within range 0 to 8.
        2. The target square is currently empty ("").
        3. The game has not already ended (no winner and not a draw).
        """
        if not isinstance(position, int):
            return False
        if position < 0 or position >= 9:
            return False
        if self.winner is not None or self.is_draw:
            return False
        if self.board[position] != "":
            return False
        return True

    def make_move(self, position):
        """
        Place the current player's mark on the board.
        
        Returns True if the move succeeded, or False if the move was invalid.
        """
        if not self.is_valid_move(position):
            return False

        # Place the mark of the current player
        self.board[position] = self.current_player
        self.move_count += 1

        # Check if this move ended the game
        self._check_game_over()

        # If game is still ongoing, switch to the other player
        if not self.winner and not self.is_draw:
            self.current_player = "O" if self.current_player == "X" else "X"

        return True

    def get_available_moves(self):
        """Return a list of indices (0 to 8) that are still empty."""
        return [i for i, cell in enumerate(self.board) if cell == ""]

    def _check_game_over(self):
        """
        Evaluate if a player has aligned three marks or if the game is a draw.
        """
        # 1. Check all 8 winning combinations
        for combo in self.WINNING_COMBINATIONS:
            a, b, c = combo
            mark = self.board[a]
            if mark != "" and mark == self.board[b] and mark == self.board[c]:
                self.winner = mark
                self.winning_combo = combo
                return

        # 2. Check for draw (all 9 squares filled and no winner)
        if "" not in self.board:
            self.is_draw = True

    def to_dict(self):
        """
        Serialize game state into a dictionary suitable for JSON responses.
        """
        return {
            "board": self.board,
            "current_player": self.current_player,
            "winner": self.winner,
            "winning_combo": self.winning_combo,
            "is_draw": self.is_draw,
            "move_count": self.move_count,
        }

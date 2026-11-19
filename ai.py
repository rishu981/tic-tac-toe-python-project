"""
Artificial Intelligence module for Tic-Tac-Toe.

This module provides three AI difficulty levels:
1. Easy:   Selects a random available square.
2. Medium: Uses smart heuristics (wins if possible, blocks opponent win,
           prefers center and corners).
3. Hard:   Uses the classic Minimax algorithm (Game Theory / Recursive Search).
           This makes the AI completely unbeatable.
"""

import random


def get_ai_move(board, ai_player="O", human_player="X", difficulty="hard"):
    """
    Select the best move for the AI based on the chosen difficulty level.
    
    :param board: List of 9 strings representing the board state (e.g. ["X", "", "O", ...])
    :param ai_player: The mark used by AI ('O')
    :param human_player: The mark used by human ('X')
    :param difficulty: 'easy', 'medium', or 'hard'
    :return: An integer index (0-8) representing the chosen position.
    """
    available_moves = [i for i, spot in enumerate(board) if spot == ""]

    if not available_moves:
        return None

    if difficulty == "easy":
        return _get_easy_move(available_moves)
    elif difficulty == "medium":
        return _get_medium_move(board, available_moves, ai_player, human_player)
    else:  # 'hard' / default
        return _get_minimax_move(board, available_moves, ai_player, human_player)


# =====================================================================
# 1. EASY AI (Random Choice)
# =====================================================================
def _get_easy_move(available_moves):
    """Pick any valid random empty square."""
    return random.choice(available_moves)


# =====================================================================
# 2. MEDIUM AI (Rule-Based Heuristic)
# =====================================================================
def _get_medium_move(board, available_moves, ai_player, human_player):
    """
    Heuristic-based decision making:
    1. If AI can win in the next move, take it.
    2. If human is about to win in the next move, block it.
    3. Take the center (position 4) if open.
    4. Take a corner (0, 2, 6, 8) if open.
    5. Take any remaining open side.
    """
    # Rule 1: Win if possible
    for move in available_moves:
        board_copy = list(board)
        board_copy[move] = ai_player
        if _check_winner(board_copy) == ai_player:
            return move

    # Rule 2: Block human winning move
    for move in available_moves:
        board_copy = list(board)
        board_copy[move] = human_player
        if _check_winner(board_copy) == human_player:
            return move

    # Rule 3: Prefer Center
    if 4 in available_moves:
        return 4

    # Rule 4: Prefer Corners
    corners = [m for m in [0, 2, 6, 8] if m in available_moves]
    if corners:
        return random.choice(corners)

    # Rule 5: Fallback to any available move
    return random.choice(available_moves)


# =====================================================================
# 3. HARD AI (Minimax Algorithm)
# =====================================================================
def _get_minimax_move(board, available_moves, ai_player, human_player):
    """
    Find the optimal move using the Minimax recursive backtracking algorithm.
    The AI acts as the Maximizer (+10 score), while the human acts as Minimizer (-10 score).
    """
    # Shortcut: If the board is completely empty, taking the center or a corner is optimal.
    # Picking instantly saves 9! (362,880) recursive function calls on move 1.
    if len(available_moves) == 9:
        return 4  # Center is the strongest opening move

    best_score = float("-inf")
    best_move = available_moves[0]

    for move in available_moves:
        board[move] = ai_player
        # Call minimax for the human player's turn (minimizing step)
        score = _minimax(board, depth=0, is_maximizing=False, ai_player=ai_player, human_player=human_player)
        board[move] = ""  # Backtrack / undo move

        if score > best_score:
            best_score = score
            best_move = move

    return best_move


def _minimax(board, depth, is_maximizing, ai_player, human_player):
    """
    Recursive Minimax Function.
    
    Evaluates every possible future state:
    - AI win:    +10 - depth  (prefers faster wins)
    - Human win: -10 + depth  (prefers delaying losses)
    - Draw:      0
    """
    winner = _check_winner(board)
    if winner == ai_player:
        return 10 - depth
    elif winner == human_player:
        return -10 + depth

    available_moves = [i for i, spot in enumerate(board) if spot == ""]
    if not available_moves:
        return 0  # Draw / Tie

    if is_maximizing:
        # AI's turn: maximize the score
        max_eval = float("-inf")
        for move in available_moves:
            board[move] = ai_player
            eval_score = _minimax(board, depth + 1, False, ai_player, human_player)
            board[move] = ""  # Backtrack
            max_eval = max(max_eval, eval_score)
        return max_eval
    else:
        # Human's turn: minimize the AI's score
        min_eval = float("inf")
        for move in available_moves:
            board[move] = human_player
            eval_score = _minimax(board, depth + 1, True, ai_player, human_player)
            board[move] = ""  # Backtrack
            min_eval = min(min_eval, eval_score)
        return min_eval


# =====================================================================
# WINNER CHECKER HELPER (Used by AI simulations)
# =====================================================================
WINNING_LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Horizontal rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Vertical columns
    (0, 4, 8), (2, 4, 6)              # Diagonals
]


def _check_winner(board):
    """Quickly check if there is a winner on the given board."""
    for a, b, c in WINNING_LINES:
        if board[a] and board[a] == board[b] == board[c]:
            return board[a]
    return None

"""
Tic-Tac-Toe Web Server.

Built entirely using Python's standard library (http.server and json).
No external frameworks (like Flask or Django) are needed.

Architecture:
- Backend: Python handles all game logic, state management, move validation,
  and the Minimax AI algorithm.
- Frontend: HTML, CSS, and minimal JavaScript communicate with Python using a
  JSON REST API.
"""

import json
from functools import partial
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlsplit

from ai import get_ai_move
from game_logic import TicTacToeGame

HOST = "127.0.0.1"
PORT = 8000
STATIC_DIRECTORY = Path(__file__).parent / "static"


class GameSession:
    """
    Manages the persistent state for the game session:
    - The active Tic-Tac-Toe board (via TicTacToeGame).
    - Game mode ('pvp' or 'pvc').
    - Computer difficulty level ('easy', 'medium', or 'hard').
    - Win / loss / draw score totals.
    """

    def __init__(self):
        self.game = TicTacToeGame()
        self.mode = "pvc"              # Default: Player vs Computer
        self.difficulty = "hard"       # Default: Unbeatable Minimax AI
        self.scores = {"X": 0, "O": 0, "draws": 0}
        self.round_number = 1

    def get_state(self):
        """Assemble complete game state for frontend rendering."""
        state = self.game.to_dict()
        state.update({
            "mode": self.mode,
            "difficulty": self.difficulty,
            "scores": self.scores,
            "round_number": self.round_number,
        })
        return state

    def set_settings(self, mode=None, difficulty=None):
        """
        Update the game mode or AI difficulty.
        Resets the current round to apply new rules fairly.
        """
        changed = False
        if mode in ("pvp", "pvc") and mode != self.mode:
            self.mode = mode
            changed = True

        if difficulty in ("easy", "medium", "hard") and difficulty != self.difficulty:
            self.difficulty = difficulty
            changed = True

        if changed:
            self.new_game()
        return True

    def play_move(self, position):
        """
        Execute a human move, followed by the computer move if in 'pvc' mode.
        Returns True if move was accepted, False otherwise.
        """
        # Block human if it is computer's turn in PvC mode
        if self.mode == "pvc" and self.game.current_player != "X":
            return False

        # Attempt to make player's move
        if not self.game.make_move(position):
            return False

        self._record_result_if_ended()

        # If playing against computer and game is still ongoing, trigger AI move
        if (
            self.mode == "pvc"
            and not self.game.winner
            and not self.game.is_draw
            and self.game.current_player == "O"
        ):
            ai_move = get_ai_move(
                board=self.game.board,
                ai_player="O",
                human_player="X",
                difficulty=self.difficulty,
            )
            if ai_move is not None:
                self.game.make_move(ai_move)
                self._record_result_if_ended()

        return True

    def new_game(self):
        """Clear the board and start a new round without resetting scores."""
        self.game.reset()
        self.round_number += 1

    def reset_scores(self):
        """Reset scoreboard back to 0 and start a fresh match."""
        self.scores = {"X": 0, "O": 0, "draws": 0}
        self.round_number = 1
        self.game.reset()

    def _record_result_if_ended(self):
        """Update scores if the round reached a terminal state."""
        if self.game.winner:
            self.scores[self.game.winner] += 1
        elif self.game.is_draw:
            self.scores["draws"] += 1


# Global single-session instance for the local player
SESSION = GameSession()


class GameRequestHandler(SimpleHTTPRequestHandler):
    """
    HTTP Request Handler that:
    1. Serves static files (HTML, CSS, JS) from the 'static' folder.
    2. Provides REST API endpoints (/api/...) for game actions.
    """

    def end_headers(self):
        """Disable browser caching so frontend updates immediately."""
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

    def _send_json(self, data, status=200):
        """Helper to send a JSON HTTP response."""
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_json(self):
        """Safely parse incoming JSON body from POST requests."""
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            self._send_json({"error": "Invalid Content-Length header."}, 400)
            return None

        if length == 0:
            return {}

        if length > 8192:
            self._send_json({"error": "Payload size too large."}, 400)
            return None

        try:
            raw_data = self.rfile.read(length).decode("utf-8")
            data = json.loads(raw_data) if raw_data.strip() else {}
        except (UnicodeDecodeError, json.JSONDecodeError):
            self._send_json({"error": "Malformed JSON payload."}, 400)
            return None

        if not isinstance(data, dict):
            self._send_json({"error": "JSON body must be an object."}, 400)
            return None

        return data

    def do_GET(self):
        """Handle GET requests: Return state or serve static frontend files."""
        path = urlsplit(self.path).path
        if path == "/api/state":
            self._send_json(SESSION.get_state())
        elif path == "/api/new-game":
            SESSION.new_game()
            self._send_json(SESSION.get_state())
        elif path == "/api/reset-scores":
            SESSION.reset_scores()
            self._send_json(SESSION.get_state())
        elif path.startswith("/api/"):
            self._send_json({"error": "Endpoint not found."}, 404)
        else:
            # Delegate to built-in SimpleHTTPRequestHandler for index.html, style.css, app.js
            super().do_GET()

    def do_POST(self):
        """Handle POST requests: Process player actions."""
        path = urlsplit(self.path).path
        data = self._read_json()
        if data is None:
            return

        if path == "/api/move":
            position = data.get("position")
            if not isinstance(position, int) or not SESSION.play_move(position):
                self._send_json({"error": "Invalid or illegal move."}, 400)
                return

        elif path == "/api/settings":
            mode = data.get("mode")
            difficulty = data.get("difficulty")
            SESSION.set_settings(mode=mode, difficulty=difficulty)

        elif path == "/api/new-game":
            SESSION.new_game()

        elif path == "/api/reset-scores":
            SESSION.reset_scores()

        else:
            self._send_json({"error": "Endpoint not found."}, 404)
            return

        # Always return the freshly updated state
        self._send_json(SESSION.get_state())


def main():
    """Start the Python HTTP server and listen on localhost:8000."""
    handler = partial(GameRequestHandler, directory=str(STATIC_DIRECTORY))
    server = HTTPServer((HOST, PORT), handler)
    print("=" * 60)
    print(f" Python Tic-Tac-Toe Server started successfully!")
    print(f" URL: http://{HOST}:{PORT}")
    print(f" Pure Python standard library • Zero external dependencies")
    print(f" Press Ctrl+C in this terminal to stop the server.")
    print("=" * 60)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped gracefully.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()

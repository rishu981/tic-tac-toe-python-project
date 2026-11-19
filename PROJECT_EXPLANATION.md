# 🎓 College Project Explanation & Viva Guide: Tic-Tac-Toe Web App

> **Project Title:** Web-Based Tic-Tac-Toe with Python REST Backend & Minimax Artificial Intelligence  
> **Core Language:** Python 3 (Standard Library — Zero External Dependencies)  
> **Frontend:** Pure HTML5, CSS3, and Vanilla JavaScript (Fetch API)  
> **Design Pattern:** Client-Server Architecture / RESTful API / Model-View-Controller (MVC)

---

## 📌 Table of Contents
1. [Project Overview & Key Highlights](#1-project-overview--key-highlights)
2. [System Architecture (Client-Server / MVC)](#2-system-architecture)
3. [File-by-File Detailed Explanation](#3-file-by-file-detailed-explanation)
   - [A. `game_logic.py` (The Model)](#a-game_logicpy)
   - [B. `ai.py` (Minimax Algorithm & Heuristics)](#b-aipy)
   - [C. `main.py` (The Controller & HTTP Server)](#c-mainpy)
   - [D. `static/index.html` (The Structure)](#d-staticindexhtml)
   - [E. `static/style.css` (The Presentation)](#e-staticstylecss)
   - [F. `static/app.js` (The Client Controller)](#f-staticappjs)
4. [Step-by-Step Execution Lifecycle of a Click](#4-step-by-step-execution-lifecycle-of-a-click)
5. [How to Run and Demonstrate](#5-how-to-run-and-demonstrate)
6. [Top 15 Viva / Teacher Interview Questions & Model Answers](#6-top-15-viva--teacher-interview-questions--answers)

---

## 1. Project Overview & Key Highlights

This project is a full-featured, interactive Tic-Tac-Toe game developed to demonstrate foundational computer science and software engineering principles:

- **100% Python Core Logic:** All game rules, turn alternation, move validation, win/draw checking, and AI decision-making reside exclusively in Python.
- **Zero Third-Party Packages:** Developed using only Python's built-in standard library (`http.server`, `json`, `random`, `urllib`). No `pip install` required!
- **Artificial Intelligence with 3 Difficulties:**
  1. *Easy:* Random selection among remaining empty squares.
  2. *Medium:* Heuristic-based (immediate win detection, blocking opponent wins, corner/center prioritization).
  3. *Hard:* **Minimax Algorithm** — a recursive game-theory algorithm that guarantees the computer is **unbeatable** (the best a human can achieve is a draw).
- **Separation of Concerns (SoC):** Clean decoupling between Backend (Python), Frontend Presentation (HTML/CSS), and Client Communication (Vanilla JS).

---

## 2. System Architecture

The application implements a classic **Client-Server Architecture**:

```
+-----------------------------------------------------------+
|                   FRONTEND (Browser Client)               |
|                                                           |
|  [HTML5 Structure]      [CSS3 Styling]     [app.js]       |
|  index.html             style.css          Fetch API      |
+-----------------------------------------------------------+
                             |  ^
           HTTP POST / GET   |  |  JSON Response
             (REST API)      v  |  {"board": [...], ...}
+-----------------------------------------------------------+
|                   BACKEND (Python Server)                 |
|                                                           |
|       main.py (http.server.HTTPServer & RequestHandler)   |
|                               ^                           |
|               +---------------+---------------+           |
|               |                               |           |
|               v                               v           |
|       game_logic.py (Rules/State)         ai.py (Minimax) |
+-----------------------------------------------------------+
```

### Why this is great for an evaluation:
1. **Model:** `game_logic.py` manages the board data and validation.
2. **View:** `index.html` and `style.css` render the interface.
3. **Controller:** `main.py` processes incoming HTTP requests, routes them to the Model and AI, and responds with JSON data.

---

## 3. File-by-File Detailed Explanation

### A. `game_logic.py`
**Purpose:** Manages the game board, player turns, and win/draw evaluation using Object-Oriented Programming (OOP).

#### 1. Board Representation:
The 3x3 grid is represented as a single flat 1D list of 9 elements:
```
Indices:
[0, 1, 2]   -> Row 0
[3, 4, 5]   -> Row 1
[6, 7, 8]   -> Row 2
```
*Why flat list?* A 1D list indexed from 0 to 8 requires simpler indexing, fewer memory allocations, and faster iteration than a nested 2D matrix (`board[r][c]`).

#### 2. Class `TicTacToeGame`:
- `self.board = [""] * 9`: Holds `""` (empty), `"X"`, or `"O"`.
- `self.current_player`: Tracks whose turn it is (`"X"` begins by convention).
- `self.winner`: Stores `"X"`, `"O"`, or `None`.
- `self.winning_combo`: Holds the indices of the three winning squares (e.g. `[0, 1, 2]`) for UI highlighting.
- `self.is_draw`: Boolean set to `True` when all squares are filled without a winner.

#### 3. Key Methods:
- `is_valid_move(position)`: Checks boundary limits (`0 <= pos <= 8`), ensures the target square is currently empty (`""`), and verifies the round has not already ended.
- `make_move(position)`: Places the player's mark, increments move count, checks if this move won or tied the game, and if ongoing, switches `self.current_player` between `"X"` and `"O"`.
- `_check_game_over()`: Iterates through the 8 possible winning lines:
  - 3 Horizontal: `(0,1,2)`, `(3,4,5)`, `(6,7,8)`
  - 3 Vertical: `(0,3,6)`, `(1,4,7)`, `(2,5,8)`
  - 2 Diagonal: `(0,4,8)`, `(2,4,6)`
  If all 3 positions have matching non-empty marks, it sets `self.winner`. Otherwise, if `"" not in self.board`, it sets `is_draw = True`.
- `to_dict()`: Serializes internal state into a Python dictionary, easily converted to JSON for the web browser.

---

### B. `ai.py`
**Purpose:** Generates intelligent moves for the computer player.

#### 1. Easy Mode (`_get_easy_move`):
- Uses Python's `random.choice(available_moves)`.
- Simulates a novice player making arbitrary legal moves.

#### 2. Medium Mode (`_get_medium_move`):
- Implements a rule-based heuristic:
  1. **Win:** If the AI has 2 in a row, take the 3rd to win immediately.
  2. **Block:** If the human has 2 in a row, take the 3rd to block the human from winning.
  3. **Center:** Take index 4 (the strongest strategic cell on the board).
  4. **Corners:** Pick any open corner (`0, 2, 6, 8`).
  5. **Sides:** Pick any remaining open square.

#### 3. Hard Mode: The Minimax Algorithm (`_get_minimax_move` & `_minimax`):
Minimax is a classic decision-rule algorithm from Artificial Intelligence and Game Theory used for two-player, zero-sum, perfect-information games.

```
                      Current Board State
                     /         |         \
               Move 1       Move 2      Move 3  (AI Maximizing: score +10)
               /    \       /    \      /    \
             H1      H2   H1      H2  H1      H2 (Human Minimizing: score -10)
```

- **Objective:**
  - AI is the **Maximizer** (aims for maximum score: `+10`).
  - Human is the **Minimizer** (aims for minimum score: `-10`).
  - Draw returns score `0`.
- **Depth Penalty (`10 - depth` and `-10 + depth`):**
  - Subtracting depth motivates the AI to win in fewer turns (e.g. win in 1 move scores `10 - 1 = 9`, win in 3 moves scores `10 - 3 = 7`).
  - Adding depth motivates the AI to delay losses if unavoidable.
- **Recursive Backtracking:**
  1. Simulate placing a mark at square `i`.
  2. Recursively evaluate the resulting board.
  3. Undo the mark (`board[i] = ""`).
  4. Pick the move that yields the highest minimax value.
- **Opening Move Optimization:**
  When all 9 squares are empty, computing Minimax traverses $9! = 362,880$ permutations. By hardcoding the first move to center (index 4), the AI plays instantly with 0ms delay while remaining mathematically optimal.

---

### C. `main.py`
**Purpose:** Web server and REST API controller.

#### 1. Why `http.server` over Flask/Django?
- Standard library modules demonstrate fundamental socket and HTTP protocol understanding without relying on heavyweight frameworks.
- Runs on any standard Python installation instantly.

#### 2. Class `GameSession`:
- Encapsulates the overall match: the current `TicTacToeGame` instance, selected mode (`"pvc"` or `"pvp"`), AI difficulty (`"easy"`, `"medium"`, `"hard"`), and cumulative scores (`X`, `O`, `draws`).
- When a human plays a move in `"pvc"` mode, `play_move()` automatically calls `get_ai_move()` from `ai.py` and applies the computer's turn in sequence before returning the updated state.

#### 3. Class `GameRequestHandler(SimpleHTTPRequestHandler)`:
- `do_GET()`:
  - If URL is `/api/state`, serializes and returns the current game state as JSON.
  - For static assets (`index.html`, `style.css`, `app.js`), delegates to Python's built-in file server.
- `do_POST()`:
  - Parses JSON request bodies using `self.rfile.read(Content-Length)`.
  - Routes to corresponding endpoints:
    - `/api/move`: Applies a move for index `0-8`.
    - `/api/settings`: Updates mode and difficulty.
    - `/api/new-game`: Clears board for a new round (keeps scores).
    - `/api/reset-scores`: Resets score counters to zero.
  - Sends back the fresh game state in standard JSON format with HTTP 200 OK.

---

### D. `static/index.html`
**Purpose:** Provides clean, accessible semantic HTML5 markup.
- Semantic elements: `<main>`, `<header>`, `<section>`, `<select>`, `<button>`.
- Responsive viewport meta tag for mobile screens.
- Accessible ARIA labels (`role="status"`, `aria-label`).
- Contains no hardcoded game outcomes; all elements dynamically update via JavaScript.

---

### E. `static/style.css`
**Purpose:** Modern, dark-themed styling with responsive design.
- **CSS Custom Properties (Variables):** Standardized color palette (`--color-x: #38bdf8`, `--color-o: #f43f5e`, `--color-win: #10b981`).
- **CSS Grid:** 3x3 layout with `grid-template-columns: repeat(3, 1fr)` and `aspect-ratio: 1` keeps squares perfectly square on all screen resolutions.
- **Distinct Mark Styling:** Targets `[data-mark="X"]` and `[data-mark="O"]` directly, ensuring each player has an identifiable neon color scheme.
- **Winning Animation:** Pulsing glowing green effect (`@keyframes pulse`) along the 3 winning tiles.

---

### F. `static/app.js`
**Purpose:** Client-side event dispatcher and DOM updater.
- Uses standard modern `async/await` and `fetch()` API.
- Implements `isRequestPending` flag to avoid rapid double-clicks while the server is processing.
- Handles user events: click on cell, change game mode, change difficulty, click new round, click reset.
- Updates the DOM based on the state dictionary received from Python.

---

## 4. Step-by-Step Execution Lifecycle of a Click

When a user clicks on the center square (index 4) against the Computer:

```
1. USER CLICKS SQUARE 4
   └── JavaScript click event fires on button[data-index="4"]

2. FETCH REQUEST SENT
   └── app.js sends HTTP POST to http://127.0.0.1:8000/api/move
       Payload: {"position": 4}

3. PYTHON SERVER PROCESSES REQUEST
   └── GameRequestHandler.do_POST() intercepts "/api/move"
   └── Parses JSON body -> extracts position: 4

4. GAME LOGIC VERIFICATION
   └── TicTacToeGame.make_move(4) validates:
       - 4 is within [0, 8]
       - board[4] is empty
       - No winner yet
   └── board[4] becomes "X"
   └── Switches current_player to "O"

5. ARTIFICIAL INTELLIGENCE EXECUTION
   └── Session detects mode is "pvc" and current_player is "O"
   └── Calls ai.get_ai_move(board, ai_player="O", difficulty="hard")
   └── Minimax simulates future moves recursively
   └── AI selects optimal move (e.g., corner 0)
   └── board[0] becomes "O"
   └── Checks game status, switches current_player back to "X"

6. JSON RESPONSE RETURNED
   └── Python serializes updated board, scores, and status into JSON
   └── Sends HTTP 200 OK back to browser

7. DOM UPDATE (RENDER)
   └── app.js receives JSON state
   └── Square 4 displays "X" (cyan), Square 0 displays "O" (red)
   └── Board is re-enabled for the human player's next move
```

---

## 5. How to Run and Demonstrate

1. Open your terminal in the project directory:
   ```bash
   cd "c:\Users\RISHU\tic tac toe"
   ```
2. Run the Python application:
   ```bash
   python main.py
   ```
3. Open your web browser and navigate to:
   **`http://127.0.0.1:8000`**
4. To demonstrate to your teacher:
   - **Mode Demonstration:** Switch between **Player vs Computer** and **Player vs Player**.
   - **AI Difficulty Demonstration:**
     - Select **Easy**: Show how the computer makes random moves and is easy to defeat.
     - Select **Medium**: Show how the computer blocks you if you have 2 in a row.
     - Select **Hard (Minimax)**: Try your best to win. Point out that the Minimax algorithm calculates every outcome, making it mathematically impossible to lose.

---

## 6. Top 15 Viva / Teacher Interview Questions & Answers

### Q1: Why did you use Python for the core logic instead of doing it all in JavaScript?
> **Answer:** "In real-world applications, client-side code running in the browser can be modified or manipulated by users. Placing the core game rules, move validation, and AI logic on the Python backend ensures security, centralized state management, and separation of concerns. It also allows us to run computationally intensive algorithms like Minimax in Python."

### Q2: Why did you use `http.server` instead of Flask or Django?
> **Answer:** "Using Python's standard library `http.server` demonstrates an understanding of fundamental web protocols, raw HTTP request/response lifecycles, headers, and REST architecture without hiding behind third-party abstractions. Additionally, it requires zero external dependencies (`pip install`), making it completely portable."

### Q3: How does the Minimax algorithm work?
> **Answer:** "Minimax is a recursive backtracking algorithm used in two-player zero-sum games. The AI acts as the 'Maximizer' trying to get the highest score (+10), while the opponent acts as the 'Minimizer' trying to minimize the AI's score (-10). Minimax explores the game tree down to terminal states (win, loss, draw) and propagates the optimal value back up to pick the move with the highest guaranteed payoff."

### Q4: What is the purpose of the `depth` parameter in Minimax?
> **Answer:** "Depth represents how many turns in the future a terminal state is reached. By scoring an AI win as `+10 - depth`, a win in 1 move scores 9 while a win in 3 moves scores 7. This forces the AI to choose the fastest route to victory rather than delaying an obvious win."

### Q5: What is the time complexity of the Minimax algorithm in Tic-Tac-Toe?
> **Answer:** "In the worst case without optimizations, Minimax explores all permutations of the 9 squares, which is $O(b^d)$ or at most $9! = 362,880$ states. Because Tic-Tac-Toe has a very small state space compared to Chess or Go, the search completes in milliseconds. We also optimized the very first move to automatically take the center or a corner, bypassing unnecessary calculations on an empty board."

### Q6: How do the frontend and backend communicate?
> **Answer:** "They communicate via a RESTful API using JSON over HTTP. The JavaScript frontend uses the standard `fetch()` API to send asynchronous HTTP POST requests (e.g. `/api/move` with `{position: 4}`). The Python backend processes the request and responds with an HTTP 200 containing the serialized game state JSON, which the browser renders."

### Q7: What data structure did you use to represent the Tic-Tac-Toe board?
> **Answer:** "We used a 1-dimensional Python list of length 9 (`[''] * 9`), where index 0 is top-left and index 8 is bottom-right. A 1D list is simpler, faster to iterate, and easier to serialize to JSON than a 2D matrix (`board[row][col]`)."

### Q8: How do you detect if someone has won the game?
> **Answer:** "There are exactly 8 possible winning lines in a 3x3 grid: 3 rows, 3 columns, and 2 diagonals. In `_check_game_over()`, we store these 8 index tuples. After each move, we check if any combination has identical, non-empty marks."

### Q9: What happens if a player tries to click an already occupied square?
> **Answer:** "There is two-layer validation:
> 1. Client-side: The button is disabled once filled.
> 2. Server-side: `TicTacToeGame.is_valid_move()` checks `self.board[position] == ''`. If illegal, the server rejects the request with HTTP 400 Bad Request. Server-side validation prevents API tampering."

### Q10: What Object-Oriented Programming (OOP) concepts are used here?
> **Answer:**
> - **Encapsulation:** The `TicTacToeGame` class encapsulates the board state, move counts, and winning logic, exposing clean methods like `make_move()` and `reset()`.
> - **Abstraction:** The HTTP server interacts with the game only through high-level methods without needing to manipulate internal array elements directly.
> - **Single Responsibility Principle:** `game_logic.py` handles rules, `ai.py` handles intelligence, and `main.py` handles networking.

### Q11: How do you prevent race conditions when a user rapidly double-clicks?
> **Answer:** "In `app.js`, we use an `isRequestPending` boolean flag. While a fetch request is in transit, further clicks are ignored, and board buttons are disabled until the server's response arrives."

### Q12: How is the score maintained across multiple rounds?
> **Answer:** "The `GameSession` class in `main.py` maintains a persistent dictionary `self.scores = {'X': 0, 'O': 0, 'draws': 0}`. When a round ends, `_record_result_if_ended()` increments the corresponding counter. The 'New Round' button clears only the board, while 'Reset Scores' resets the counters."

### Q13: Can you explain the difference between GET and POST in your API?
> **Answer:**
> - `GET /api/state`: Safe, idempotent read operation used when the page loads to fetch the current board and scores.
> - `POST /api/move`, `/api/settings`, etc.: State-mutating operations that transmit a request body (payload) to change server state.

### Q14: How does the Medium AI differ from the Hard AI?
> **Answer:** "Medium AI uses a greedy, rule-based heuristic: it checks for an immediate win, blocks an immediate opponent win, and otherwise chooses center/corners. Hard AI uses full tree search (Minimax), looking multiple moves ahead to ensure it cannot be trapped into a fork."

### Q15: If you had more time, what improvements would you add?
> **Answer:** "We could add Alpha-Beta Pruning to optimize the Minimax tree search, WebSockets for real-time multiplayer over a local area network (LAN), and persistent score storage in an SQLite database."

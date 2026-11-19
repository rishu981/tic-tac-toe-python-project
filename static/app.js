/**
 * Tic-Tac-Toe Frontend Controller (Vanilla JavaScript)
 *
 * NOTE FOR COLLEGE PRESENTATION:
 * The frontend contains NO game rules or AI logic.
 * It strictly acts as the "View" and "Controller":
 * 1. Captures user interactions (clicks, dropdown changes).
 * 2. Sends HTTP requests (via Fetch API) to the Python backend.
 * 3. Updates the HTML DOM with the JSON state returned by Python.
 */

// DOM Elements
const boardElement = document.querySelector(".board");
const squares = Array.from(document.querySelectorAll(".square"));
const modeSelect = document.querySelector("#mode");
const difficultySelect = document.querySelector("#difficulty");
const difficultyGroup = document.querySelector("#difficulty-group");
const statusMessage = document.querySelector("#status");
const xScore = document.querySelector("#x-score");
const oScore = document.querySelector("#o-score");
const drawScore = document.querySelector("#draw-score");
const oTitle = document.querySelector("#o-title");
const oLabel = document.querySelector("#o-label");
const newGameBtn = document.querySelector("#new-game");
const resetScoresBtn = document.querySelector("#reset-scores");

// State flag to prevent rapid double-clicks while network request is in flight
let isRequestPending = false;

/**
 * Send an HTTP POST request to the Python backend.
 * @param {string} url - API endpoint path (e.g. '/api/move')
 * @param {object} [data] - JSON body object
 * @returns {Promise<object>} - Parsed JSON response from Python
 */
async function postAPI(url, data = {}) {
  const response = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Cache-Control": "no-cache",
    },
    body: JSON.stringify(data),
  });

  const result = await response.json();
  if (!response.ok) {
    throw new Error(result.error || "Server error occurred");
  }
  return result;
}

/**
 * Fetch current state via GET.
 */
async function getAPI(url) {
  const response = await fetch(url, {
    method: "GET",
    headers: { "Cache-Control": "no-cache" },
  });
  const result = await response.json();
  if (!response.ok) {
    throw new Error(result.error || "Server error occurred");
  }
  return result;
}

/**
 * Display an error message banner to the user.
 */
function showError(message) {
  statusMessage.textContent = message;
  statusMessage.classList.add("error");
}

/**
 * Render the complete game UI based on the state received from Python.
 * @param {object} state - Game state dictionary from Python server
 */
function render(state) {
  // 1. Sync dropdowns without triggering change events
  if (modeSelect.value !== state.mode) {
    modeSelect.value = state.mode;
  }
  if (difficultySelect.value !== state.difficulty) {
    difficultySelect.value = state.difficulty;
  }

  // Show or hide difficulty selector based on mode
  if (state.mode === "pvc") {
    difficultyGroup.style.display = "flex";
    oTitle.textContent = "COMPUTER (O)";
    oLabel.textContent = `AI: ${state.difficulty.toUpperCase()}`;
  } else {
    difficultyGroup.style.display = "none";
    oTitle.textContent = "PLAYER O";
    oLabel.textContent = "Opponent";
  }

  // 2. Update Scoreboard
  xScore.textContent = state.scores.X;
  oScore.textContent = state.scores.O;
  drawScore.textContent = state.scores.draws;

  // 3. Update the 3x3 Grid
  const isGameOver = Boolean(state.winner) || state.is_draw;

  squares.forEach((square, index) => {
    const mark = state.board[index] || "";
    square.textContent = mark;
    square.dataset.mark = mark; // Used by CSS for coloring X vs O

    // Highlight winning squares
    const isWinningCell = state.winning_combo && state.winning_combo.includes(index);
    square.classList.toggle("winning", Boolean(isWinningCell));

    // Disable square only if already marked or game is over
    square.disabled = Boolean(mark) || isGameOver;
  });

  // 4. Update Status Banner
  statusMessage.classList.remove("error");

  if (state.winner) {
    if (state.mode === "pvc") {
      statusMessage.textContent =
        state.winner === "X" ? "🎉 You Won the Game!" : "🤖 Computer Won the Game!";
    } else {
      statusMessage.textContent = `🎉 Player ${state.winner} Wins!`;
    }
  } else if (state.is_draw) {
    statusMessage.textContent = "🤝 Game ended in a Draw!";
  } else {
    if (state.mode === "pvc") {
      statusMessage.textContent = "Your Turn (X)";
    } else {
      statusMessage.textContent = `Player ${state.current_player}'s Turn`;
    }
  }
}

/**
 * Execute an API action safely with busy state management.
 */
async function handleAction(endpoint, payload = {}) {
  if (isRequestPending) return;
  isRequestPending = true;
  boardElement.classList.add("busy");

  try {
    const newState = await postAPI(endpoint, payload);
    render(newState);
  } catch (err) {
    showError(err.message);
  } finally {
    isRequestPending = false;
    boardElement.classList.remove("busy");
  }
}

// ---------------------------------------------------------------------
// Event Listeners (User Interaction Hooks)
// ---------------------------------------------------------------------

// Board Cell Clicks
squares.forEach((square) => {
  square.addEventListener("click", (e) => {
    e.preventDefault();
    const position = parseInt(square.dataset.index, 10);
    handleAction("/api/move", { position });
  });
});

// Mode Selection Change
modeSelect.addEventListener("change", () => {
  handleAction("/api/settings", {
    mode: modeSelect.value,
    difficulty: difficultySelect.value,
  });
});

// Difficulty Selection Change
difficultySelect.addEventListener("change", () => {
  handleAction("/api/settings", {
    mode: modeSelect.value,
    difficulty: difficultySelect.value,
  });
});

// New Round Button
newGameBtn.addEventListener("click", (e) => {
  e.preventDefault();
  handleAction("/api/new-game", {});
});

// Reset Scores Button
resetScoresBtn.addEventListener("click", (e) => {
  e.preventDefault();
  handleAction("/api/reset-scores", {});
});

// Initial Page Load: Fetch current state from Python server
getAPI("/api/state")
  .then(render)
  .catch((err) => showError("Could not connect to Python server: " + err.message));

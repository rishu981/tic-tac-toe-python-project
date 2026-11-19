# 🎮 Tic-Tac-Toe (Python + Minimax AI)

A clean, modern web-based Tic-Tac-Toe application developed for a college demonstration. Built with **100% pure Python standard library** for all core logic, rules, and AI decision-making, accompanied by a clean HTML5 and CSS3 interface.

---

## 🌟 Key Features
- **Pure Python Core:** Zero third-party dependencies (`no pip install` needed).
- **3 AI Difficulty Levels:**
  - **Easy:** Random legal moves.
  - **Medium:** Smart heuristic checks (win & block detection, center preference).
  - **Hard:** **Unbeatable Minimax Algorithm** (Game Theory recursive search).
- **Player vs Player & Player vs Computer:** Switch modes on the fly.
- **RESTful JSON API:** Clear separation between Python backend and browser frontend.
- **College Viva & Teacher Guide:** Complete explanation file included (`PROJECT_EXPLANATION.md`).

---

## 🚀 How to Run the Project

1. Open your terminal in this project directory:
   ```bash
   python main.py
   ```
2. Open your web browser and visit:
   ```
   http://127.0.0.1:8000
   ```
3. Press `Ctrl + C` in the terminal to stop the server when done.

---

## 📁 Project Structure

```
tic tac toe/
│
├── game_logic.py          # Core game rules, board state, win/draw checking (OOP)
├── ai.py                  # Artificial intelligence (Easy, Medium, Minimax algorithm)
├── main.py                # Built-in HTTP server & RESTful JSON API endpoints
├── PROJECT_EXPLANATION.md # Detailed college guide & 15 viva questions with answers
├── README.md              # Project overview and quick start guide
│
└── static/                # Frontend web assets
    ├── index.html         # Semantic HTML5 layout
    ├── style.css          # Responsive dark theme styling
    └── app.js             # Client controller (Fetch API communicating with Python)
```

---

## 📖 For Teacher / Viva Explanation
Please refer to the comprehensive [PROJECT_EXPLANATION.md](file:///c:/Users/RISHU/tic%20tac%20toe/PROJECT_EXPLANATION.md) file, which contains:
- Architecture and data flow diagrams.
- Line-by-line breakdown of every Python file.
- Detailed explanation of the Minimax algorithm and math.
- Top 15 teacher questions and model answers.

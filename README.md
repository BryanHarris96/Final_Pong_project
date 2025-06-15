# Pong Tournament (Pygame)

A customizable two-player Pong tournament built with Pygame. Host best-of series with human players, adjust match settings, and track all-time results.

---

## Project Proposal

**Title:** Development of a Modular Pong Game in Python  
**Student:** Bryan Harris  

**Objective:**  
Develop a fully functional and modular Pong game in Python, incorporating class concepts and extending into new areas such as game engines and sound integration.

### Overview

Inspired by a Pong implementation from 10 years ago, this project focuses on a clean, human-centered experience with refined controls, accurate score tracking, sound feedback, and configuration options. A basic AI opponent is an optional stretch goal.

---

## Core Features

1. **Modular Design**  
   - Separation of concerns with dedicated modules (game logic, UI, sound, persistence).  
   - Easy-to-maintain structure.

2. **Gameplay Mechanics**  
   - Responsive controls for two human players.  
   - Configurable match settings: point limits, best-of format.  
   - Accurate in-game scoring and HUD display.

3. **Scoreboard & Tracking**  
   - Persistent leaderboard recording match results to JSON and CSV.  
   - Display of all-time top players and recent matches.

4. **Sound Integration**  
   - Bounce and score effects triggered via Pygame mixer.  
   - Auditory feedback for paddles, walls, and scoring.

5. **AI Opponent (Stretch Goal)**  
   - Optional single-player mode with CPU-controlled paddle.  
   - Adjustable difficulty settings.

---

## New Concepts & Learning Objectives

- **Game Engine:** Use of Pygame for graphics and input handling.  
- **Sound Playback:** Integration with `pygame.mixer` for real-time effects.  
- **Data Persistence:** JSON and CSV storage for settings and leaderboard.  
- **Defensive Programming:** Validation logic and error handling.  
- **Python Fundamentals:** Functions, modules, loops, conditionals, and data structures.

---

## Installation

1. Clone the repository:  
   ```bash
   git clone https://github.com/your-username/pygame-pong-tournament.git
   cd pygame-pong-tournament
   ```

2. Create and activate a virtual environment:  
   ```bash
   python -m venv venv
   # Windows
   .\venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:  
   ```bash
   pip install pygame
   ```

4. Run the game:  
   ```bash
   python main.py
   ```

---

## Controls

- **Main Menu:**  
  - Navigate with ↑/↓ or W/S  
  - Select with Enter, Space, or mouse click  

- **Name Entry:**  
  - Click the input box, type the name, press Enter  

- **Settings:**  
  - Click `-`/`+` to adjust Matches, Games/Match, Points/Game  
  - Press Enter or click **Back** to confirm  

- **Serve Selection:**  
  - Press `1` or `2` or click to choose starting server  

- **In-Game:**  
  - Player 1: W/S (up/down)  
  - Player 2: ↑/↓ (up/down)  
  - Pause: Esc  

- **Pause Menu:**  
  - Options: Resume, Settings, Main Menu, Quit  
  - Navigate with arrows or mouse; select with Enter, Space, or click  

- **Win/Transition Screens:**  
  - Press any key or click to continue  

---

## File Structure

```
pong-tournament/
├── assets/
│   └── sounds/
│       ├── bounce.mp3
│       └── score.wav
├── constants.py
├── inputbox.py
├── main.py
├── menu.py
├── pause_menu.py
├── settings_screen.py
├── states.py
├── transition_screen.py
├── utils.py
├── win_screen.py
├── game.py
├── leaderboard.py
└── README.md
```

---

## Extensibility

- **AI Opponent:** Implement CPU paddle logic.  
- **Additional Games:** Add Snake, Asteroids, etc.  
- **Networking:** Enable multiplayer over network.  
- **Custom Themes:** Swap assets and colors for new looks.

---

## License

Licensed under the MIT License. See [LICENSE](LICENSE) for details.

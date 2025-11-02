# 🎮 COMP9001 Final Project – 2048 Game 

## 🧩 Project Overview
This is a **Python-based 2048 Game** developed as the **final project for COMP9001 (Introduction to Programming)**.  
It uses the **Tkinter** GUI library to provide an interactive interface and implements all core game logic manually (no external 2048 engine).  
This version also includes a **real-time scoring system** that tracks the player’s progress dynamically.

---

## 🚀 Features
✅ Classic **2048 gameplay** – Combine matching tiles to reach 2048.  
✅ **Keyboard control** (arrow keys or WASD).  
✅ **Real-time scoring system** – Gain points with every merge.  
✅ **Undo** feature – Press `Backspace` to undo the last move.  
✅ **Win/Lose detection** – Game automatically shows “You Win!” or “You Lose!”.  
✅ **Clean and well-documented code** – Organized into logic, constants, and GUI sections.

---

## 🕹️ Gameplay Instructions

| Key | Action |
|-----|---------|
| ↑ / W | Move Up |
| ↓ / S | Move Down |
| ← / A | Move Left |
| → / D | Move Right |
| ⌫ (Backspace) | Undo Last Move |
| Esc | Quit Game |

🎯 **Goal:** Combine numbers until you create a **2048** tile.  
Every merge increases your **score** by the value of the new tile created.

---

## 🧠 Game Logic Summary
The game uses a 4×4 matrix (`list[list[int]]`) to represent the grid.  
Each move follows these key logic steps:

1. **Cover Up** – Shift all non-zero tiles toward the move direction.  
2. **Merge** – Combine adjacent equal tiles and increase score.  
3. **Add Tile** – Randomly place a new `2` (90%) or `4` (10%) tile.  
4. **Check State** – Determine if the player won, lost, or can continue.

---

## 🖥️ Run the Game

### 🔧 Requirements
- Python 3.x  
- Tkinter (usually built-in with Python)

### ▶️ How to Run
1. Save the code file as `puzzle_2048.py`
2. Open your terminal or command prompt.
3. Navigate to the directory containing the file.
4. Run:
   ```bash
   python puzzle_2048.py
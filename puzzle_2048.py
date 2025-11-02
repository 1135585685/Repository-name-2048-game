import random
import copy
from tkinter import Frame, Label, CENTER, StringVar

# ================================================
# 1. Constants Section
# ================================================
GRID_LEN = 4
SIZE = 400
GRID_PADDING = 10
BACKGROUND_COLOR_GAME = "#92877d"
BACKGROUND_COLOR_CELL_EMPTY = "#9e948a"

# Colors for tiles
BACKGROUND_COLOR_DICT = {
    2: "#eee4da",
    4: "#ede0c8",
    8: "#f2b179",
    16: "#f59563",
    32: "#f67c5f",
    64: "#f65e3b",
    128: "#edcf72",
    256: "#edcc61",
    512: "#edc850",
    1024: "#edc53f",
    2048: "#edc22e",
}

# Text colors
CELL_COLOR_DICT = {
    2: "#776e65",
    4: "#776e65",
    8: "#f9f6f2",
    16: "#f9f6f2",
    32: "#f9f6f2",
    64: "#f9f6f2",
    128: "#f9f6f2",
    256: "#f9f6f2",
    512: "#f9f6f2",
    1024: "#f9f6f2",
    2048: "#f9f6f2",
}

FONT = ("Verdana", 24, "bold")
SCORE_FONT = ("Verdana", 14, "bold")

# Key bindings
KEY_UP = "Up"
KEY_DOWN = "Down"
KEY_LEFT = "Left"
KEY_RIGHT = "Right"
KEY_UP_ALT1 = "w"
KEY_DOWN_ALT1 = "s"
KEY_LEFT_ALT1 = "a"
KEY_RIGHT_ALT1 = "d"
KEY_UP_ALT2 = "W"
KEY_DOWN_ALT2 = "S"
KEY_LEFT_ALT2 = "A"
KEY_RIGHT_ALT2 = "D"
KEY_QUIT = "Escape"
KEY_BACK = "BackSpace"

# ================================================
# 2.  Logic Section (with score tracking)
# ================================================

def new_game(n):
    """Create a new n x n board and add two tiles."""
    mat = [[0] * n for _ in range(n)]
    mat = add_two(mat)
    mat = add_two(mat)
    return mat

def add_two(mat):
    """Add 2 or 4 randomly to an empty cell."""
    empties = [(i, j) for i in range(len(mat)) for j in range(len(mat[0])) if mat[i][j] == 0]
    if not empties:
        return mat
    i, j = random.choice(empties)
    mat[i][j] = 4 if random.random() < 0.1 else 2
    return mat

def game_state(mat):
    """Check if game is won, lost, or still playing."""
    for row in mat:
        for v in row:
            if v >= 2048:
                return 'win'
    for row in mat:
        if 0 in row:
            return 'not over'
    n = len(mat)
    # Check for possible merges
    for i in range(n):
        for j in range(n - 1):
            if mat[i][j] == mat[i][j + 1]:
                return 'not over'
    for j in range(n):
        for i in range(n - 1):
            if mat[i][j] == mat[i + 1][j]:
                return 'not over'
    return 'lose'

def reverse(mat):
    """Reverse each row."""
    return [list(reversed(row)) for row in mat]

def transpose(mat):
    """Swap rows and columns."""
    n = len(mat)
    return [[mat[i][j] for i in range(n)] for j in range(n)]

def cover_up(mat):
    """Move all tiles to the left."""
    n = GRID_LEN
    new = [[0] * n for _ in range(n)]
    done = False
    for i in range(n):
        idx = 0
        for j in range(n):
            if mat[i][j] != 0:
                if j != idx:
                    done = True
                new[i][idx] = mat[i][j]
                idx += 1
    return new, done

def merge(mat, done):
    """Merge equal tiles and count score."""
    n = GRID_LEN
    score = 0
    for i in range(n):
        for j in range(n - 1):
            if mat[i][j] != 0 and mat[i][j] == mat[i][j + 1]:
                mat[i][j] *= 2
                score += mat[i][j]
                mat[i][j + 1] = 0
                done = True
    return mat, done, score

# Move functions
def move_left(game):
    game, done = cover_up(game)
    game, done, score = merge(game, done)
    game, _ = cover_up(game)
    return game, done, score

def move_right(game):
    game = reverse(game)
    game, done = cover_up(game)
    game, done, score = merge(game, done)
    game, _ = cover_up(game)
    game = reverse(game)
    return game, done, score

def move_up(game):
    game = transpose(game)
    game, done = cover_up(game)
    game, done, score = merge(game, done)
    game, _ = cover_up(game)
    game = transpose(game)
    return game, done, score

def move_down(game):
    game = transpose(game)
    game = reverse(game)
    game, done = cover_up(game)
    game, done, score = merge(game, done)
    game, _ = cover_up(game)
    game = reverse(game)
    game = transpose(game)
    return game, done, score

# ================================================
# 3. GUI Section (Tkinter)
# ================================================
class GameGrid(Frame):
    """Game window and event handling."""
    def __init__(self):
        Frame.__init__(self)
        self.grid()
        self.master.title('2048 with Score')
        self.master.bind("<Key>", self.key_down)

        # Score setup
        self.total_score = 0
        self.score_text = StringVar()
        self.score_text.set(f"Score: {self.total_score}")

        # Score label
        self.score_label = Label(
            self,
            textvariable=self.score_text,
            font=SCORE_FONT,
            bg="#bbada0",
            fg="#f9f6f2",
            width=15,
            height=1
        )
        self.score_label.grid(row=0, column=0, columnspan=4, pady=(5, 0))

        # Key control mapping
        self.commands = {
            KEY_UP: move_up,
            KEY_DOWN: move_down,
            KEY_LEFT: move_left,
            KEY_RIGHT: move_right,
            KEY_UP_ALT1: move_up,
            KEY_DOWN_ALT1: move_down,
            KEY_LEFT_ALT1: move_left,
            KEY_RIGHT_ALT1: move_right,
            KEY_UP_ALT2: move_up,
            KEY_DOWN_ALT2: move_down,
            KEY_LEFT_ALT2: move_left,
            KEY_RIGHT_ALT2: move_right,
        }

        # Initialize grid
        self.grid_cells = []
        self.init_grid()
        self.matrix = new_game(GRID_LEN)
        self.history = []
        self.update_grid_cells()
        self.mainloop()

    def init_grid(self):
        """Draw the 4x4 grid."""
        background = Frame(self, bg=BACKGROUND_COLOR_GAME, width=SIZE, height=SIZE)
        background.grid()
        for i in range(GRID_LEN):
            grid_row = []
            for j in range(GRID_LEN):
                cell = Frame(
                    background,
                    bg=BACKGROUND_COLOR_CELL_EMPTY,
                    width=SIZE / GRID_LEN,
                    height=SIZE / GRID_LEN
                )
                cell.grid(row=i, column=j, padx=GRID_PADDING, pady=GRID_PADDING)
                t = Label(
                    master=cell, text="", bg=BACKGROUND_COLOR_CELL_EMPTY,
                    justify=CENTER, font=FONT, width=5, height=2
                )
                t.grid()
                grid_row.append(t)
            self.grid_cells.append(grid_row)

    def update_grid_cells(self):
        """Update numbers and colors."""
        for i in range(GRID_LEN):
            for j in range(GRID_LEN):
                new_number = self.matrix[i][j]
                if new_number == 0:
                    self.grid_cells[i][j].configure(text="", bg=BACKGROUND_COLOR_CELL_EMPTY)
                else:
                    bg = BACKGROUND_COLOR_DICT.get(new_number, BACKGROUND_COLOR_DICT[max(BACKGROUND_COLOR_DICT)])
                    fg = CELL_COLOR_DICT.get(new_number, CELL_COLOR_DICT[max(CELL_COLOR_DICT)])
                    self.grid_cells[i][j].configure(text=str(new_number), bg=bg, fg=fg)
        self.update_idletasks()

    def key_down(self, event):
        """Handle key events."""
        key = event.keysym

        # Quit
        if key == KEY_QUIT:
            exit()

        # Undo
        if key == KEY_BACK and self.history:
            self.matrix, self.total_score = self.history.pop()
            self.score_text.set(f"Score: {self.total_score}")
            self.update_grid_cells()
            return

        # Moves
        if key in self.commands:
            self.history.append((copy.deepcopy(self.matrix), self.total_score))
            new_matrix, done, gained = self.commands[key](self.matrix)

            if done:
                self.total_score += gained
                self.matrix = add_two(new_matrix)
                self.update_grid_cells()
                self.score_text.set(f"Score: {self.total_score}")

                # Check win or lose
                state = game_state(self.matrix)
                if state == 'win':
                    self.grid_cells[1][1].configure(text="You", bg="#9e948a")
                    self.grid_cells[1][2].configure(text="Win!", bg="#9e948a")
                elif state == 'lose':
                    self.grid_cells[1][1].configure(text="You", bg="#9e948a")
                    self.grid_cells[1][2].configure(text="Lose!", bg="#9e948a")
            else:
                self.history.pop()

if __name__ == "__main__":
    GameGrid()
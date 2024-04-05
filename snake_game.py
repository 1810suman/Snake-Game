import tkinter as tk
import random

# Constants for the game
GAME_WIDTH = 600
GAME_HEIGHT = 400
GRID_SIZE = 20
DEFAULT_DELAY = 200  # milliseconds
START_LENGTH = 3

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake Game")

        self.canvas = tk.Canvas(root, width=GAME_WIDTH, height=GAME_HEIGHT, bg='black')
        self.canvas.pack()

        self.snake = [(0, 0)]  # Snake's body as list of (x, y) coordinates
        self.direction = (1, 0)  # Initial direction: right
        self.food = self.create_food()

        self.score = 0
        self.score_label = tk.Label(root, text="Score: 0", font=('Arial', 12), fg='white', bg='black')
        self.score_label.pack()

        self.game_over_text = None
        self.game_over = False
        self.delay = DEFAULT_DELAY  # Initial delay

        # Bind arrow keys for controlling snake
        self.canvas.bind("<Left>", lambda event: self.set_direction((-1, 0)))
        self.canvas.bind("<Right>", lambda event: self.set_direction((1, 0)))
        self.canvas.bind("<Up>", lambda event: self.set_direction((0, -1)))
        self.canvas.bind("<Down>", lambda event: self.set_direction((0, 1)))

        # Set focus on the canvas
        self.canvas.focus_set()

        # Speed control settings
        self.speed_label = tk.Label(root, text="Speed", font=('Arial', 12), fg='white', bg='black')
        self.speed_label.pack()
        self.speed_scale = tk.Scale(root, from_=50, to=300, orient=tk.HORIZONTAL, length=200, command=self.update_speed)
        self.speed_scale.set(DEFAULT_DELAY)
        self.speed_scale.pack()

        # Pause button
        self.paused = False
        self.pause_button = tk.Button(root, text="Pause", command=self.toggle_pause)
        self.pause_button.pack()

        # Restart button
        self.restart_button = tk.Button(root, text="Restart", command=self.restart_game)
        self.restart_button.pack()

        self.update()

    def set_direction(self, direction):
        if not self.game_over and (direction[0] * -1, direction[1] * -1) != self.direction:  # Prevent opposite direction
            self.direction = direction

    def create_food(self):
        while True:
            food = (random.randint(0, GAME_WIDTH // GRID_SIZE - 1) * GRID_SIZE,
                    random.randint(0, GAME_HEIGHT // GRID_SIZE - 1) * GRID_SIZE)
            if food not in self.snake:
                return food

    def move_snake(self):
        if not self.paused:
            head = self.snake[-1]
            new_head = (head[0] + self.direction[0] * GRID_SIZE, head[1] + self.direction[1] * GRID_SIZE)

            # Check collision with walls or itself
            if (new_head[0] < 0 or new_head[0] >= GAME_WIDTH or
                    new_head[1] < 0 or new_head[1] >= GAME_HEIGHT or
                    new_head in self.snake):
                self.game_over = True
                return

            self.snake.append(new_head)

            # If snake eats food
            if new_head == self.food:
                self.score += 10
                self.score_label.config(text=f"Score: {self.score}")
                self.food = self.create_food()
            else:
                self.snake.pop(0)  # Remove tail

    def update(self):
        if not self.game_over:
            self.move_snake()
            self.draw_snake()
            self.draw_food()
        else:
            if self.game_over_text is None:
                self.game_over_text = self.canvas.create_text(GAME_WIDTH // 2, GAME_HEIGHT // 2,
                                                               text=f"Game Over\nScore: {self.score}",
                                                               font=('Segoe UI', 20), fill='white', justify='center')
        self.root.after(self.delay, self.update)

    def update_speed(self, delay):
        self.delay = int(delay)

    def draw_snake(self):
        self.canvas.delete("snake")
        for segment in self.snake:
            x, y = segment
            self.canvas.create_rectangle(x, y, x + GRID_SIZE, y + GRID_SIZE, fill='green', tags="snake")

    def draw_food(self):
        self.canvas.delete("food")
        x, y = self.food
        self.canvas.create_oval(x, y, x + GRID_SIZE, y + GRID_SIZE, fill='red', tags="food")

    def restart_game(self):
        self.snake = [(0, 0)]  # Reset snake position
        self.direction = (1, 0)  # Reset direction
        self.food = self.create_food()  # Reset food position
        self.score = 0  # Reset score
        self.score_label.config(text="Score: 0")
        self.game_over = False
        if self.game_over_text is not None:
            self.canvas.delete(self.game_over_text)
            self.game_over_text = None

    def toggle_pause(self):
        self.paused = not self.paused
        if self.paused:
            self.pause_button.config(text="Resume")
        else:
            self.pause_button.config(text="Pause")

def main():
    root = tk.Tk()
    snake_game = SnakeGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()

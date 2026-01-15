import tkinter as tk
import random

class PipeScreensaver:
    def __init__(self, root, num_pipes=5):
        self.root = root
        self.root.attributes('-fullscreen', True)
        self.root.config(cursor="none")
        self.root.bind("<Escape>", lambda e: self.root.destroy())

        # Stop input
        self.root.bind_all("<Key>", self.block_input)
        self.root.bind_all("<Button>", self.block_input)
        self.root.bind_all("<Motion>", self.block_input)

        self.canvas = tk.Canvas(self.root, bg="black", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()

        self.pipe_length = 40
        self.max_segments = 100

        self.pipes = [self.create_pipe() for _ in range(num_pipes)]

        self.animate()

    def block_input(self, event):
        return "break"

    def create_pipe(self):
        start_x = random.randint(100, self.width - 100)
        start_y = random.randint(100, self.height - 100)
        color = "#%06x" % random.randint(0x555555, 0xFFFFFF)
        segments = [(start_x, start_y)]
        direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        return {
            "segments": segments,
            "direction": direction,
            "color": color
        }

    def step_pipe(self, pipe):
        x, y = pipe["segments"][-1]
        dx, dy = pipe["direction"]
        new_dir = random.choice([
            d for d in [(1, 0), (-1, 0), (0, 1), (0, -1)]
            if d != (-dx, -dy)  # No direct baktraking
        ])
        pipe["direction"] = new_dir
        nx = x + new_dir[0] * self.pipe_length
        ny = y + new_dir[1] * self.pipe_length

        # Stay on screen
        nx = max(0, min(self.width, nx))
        ny = max(0, min(self.height, ny))

        pipe["segments"].append((nx, ny))
        if len(pipe["segments"]) > self.max_segments:
            pipe["segments"].pop(0)

    def draw_pipe(self, pipe):
        coords = pipe["segments"]
        for i in range(1, len(coords)):
            x1, y1 = coords[i-1]
            x2, y2 = coords[i]
            self.canvas.create_line(x1, y1, x2, y2, fill=pipe["color"], width=5)

    def animate(self):
        self.canvas.delete("all")
        for pipe in self.pipes:
            self.step_pipe(pipe)
            self.draw_pipe(pipe)
        self.root.after(50, self.animate)

def main():
    root = tk.Tk()
    PipeScreensaver(root)
    root.mainloop()

if __name__ == "__main__":
    main()
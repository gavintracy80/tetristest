import turtle
import random
import time

wn = turtle.Screen()
wn.title("Tetris by Gav")
wn.bgcolor("navy")
wn.setup(width=450, height=650)
wn.tracer(0)

delay = 0.05


class Shape():
    def __init__(self):
        self.x = 5
        self.y = 0
        self.color = random.randint(1, 7)

        square = [[1, 1],
                  [1, 1]]

        line = [[1, 1, 1, 1]]

        l_right = [[0, 0, 1],
                   [1, 1, 1]]

        l_left = [[1, 0, 0],
                  [1, 1, 1]]

        tee = [[0, 1, 0],
               [1, 1, 1]]

        l_angle = [[1, 1, 0],
                   [0, 1, 1]]

        r_angle = [[0, 1, 1],
                   [1, 1, 0]]

        shapes = [square, line, l_right, l_right,
                  l_left, tee, l_angle, r_angle]

        self.shape = random.choice(shapes)

        self.width = len(self.shape[0])
        self.height = len(self.shape)

    def rotate(self, grid):
        self.erase_shape(grid)
        temp_shape = []
        temp_row = []
        for i in range(self.width):
            for a in range(self.height-1, -1, -1):
                temp_row.append(self.shape[a][i])
            temp_shape.append(temp_row)
            temp_row = []
        right_side = self.x + len(temp_shape[0])
        if right_side < len(grid[0]) and self.x > 0:
            self.shape = temp_shape
            self.width = len(self.shape[0])
            self.height = len(self.shape)

    def move_left(self, grid):
        move = False
        if self.x > 0:
            move = True
            for y in range(self.height):
                if self.shape[y][0] == 1:
                    if grid[self.y + y][self.x - 1] != 0:
                        move = False
                        break
        if move:
            if self.y + self.height < 24 and self.can_move(grid, 0):
                self.erase_shape(grid)
            if self.can_move(grid, -1):
                self.erase_shape(grid)
            self.x -= 1

    def move_right(self, grid):
        move = False
        if self.x < 12 - self.width:
            move = True
            for y in range(self.height):
                if self.shape[y][self.width - 1] == 1:
                    if grid[self.y + y + 1][self.x + self.width] != 0:
                        move = False
                        break
        if move:
            if self.y + self.height < 24 and self.can_move(grid, 0):
                self.erase_shape(grid)
            if self.can_move(grid, 1):
                self.erase_shape(grid)
            self.x += 1

    def draw_shape(self, grid):
        for y in range(self.height):
            for x in range(self.width):
                if self.shape[y][x] == 1:
                    grid[self.y + y][self.x + x] = self.color

    def erase_shape(self, grid):
        for y in range(self.height):
            for x in range(self.width):
                if self.shape[y][x] == 1:
                    if grid[self.y + y][self.x + x] == self.color:
                        grid[self.y + y][self.x + x] = 0

    def can_move(self, grid, side_x):
        for x in range(self.width):
            if self.shape[self.height - 1][x] == 1:
                if grid[self.y + self.height][self.x + x + side_x] != 0:
                    return False

# need to clean up following:
        if self.height == 2:
            for x in range(self.width):
                if self.shape[0][x] == 1 and self.shape[1][x] == 0:
                    if grid[self.y + 1][self.x + x + side_x] != 0:
                        return False

        elif self.height == 3:
            for x in range(self.width):
                if self.shape[0][x] == 1 and self.shape[1][x] == 0:
                    if grid[self.y + 1][self.x + x + side_x] != 0:
                        return False
            for x in range(self.width):
                if self.shape[1][x] == 1 and self.shape[2][x] == 0:
                    if grid[self.y + 2][self.x + x + side_x] != 0:
                        return False

        return True


def check_grid(grid):
    y = 23
    while y >= 0:
        is_full = True
        for x in range(0, 12):
            if grid[y][x] == 0:
                is_full = False
                y -= 1
                break

        if is_full:
            score.add_score()
            for y in range(y, 0, -1):
                for x in range(0, 12):
                    grid[y][x] = grid[y-1][x]
            check_grid(grid)


grid = []
for i in range(24):
    grid.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

pen = turtle.Turtle()
pen.penup()
pen.speed(0)
pen.shape("square")
pen.setundobuffer(None)


def draw_grid(pen, grid):
    pen.clear()
    top = 230
    left = -110

    colors = ["black", "lightblue", "blue",
              "orange", "yellow", "green", "purple", "red"]

    for y in range(len(grid)):
        for x in range(len(grid[0])):
            screen_x = left + (x * 20)
            screen_y = top - (y * 20)
            pen.color("black", colors[grid[y][x]])
            pen.goto(screen_x, screen_y)
            pen.stamp()


class Score():
    score = 0

    def add_score(self):
        self.score += 10

    def draw_score(self, pen):
        pen.color("white")
        pen.hideturtle()
        pen.goto(0, -300)
        pen.write("Score {}".format(self.score), move=False,
                  align="left", font=("Arial", 24, "normal"))


def draw_game_over(pen):
    play_again = wn.textinput("Game Over", "Play Again Y/N:")
    if play_again.upper() == "Y":
        print("yes")
    elif play_again.upper() == "N":
        wn.clear()
        wn.bye()


def speed_up(delay):
    time.sleep(0)


shape = Shape()
score = Score()


wn.listen()
wn.onkeypress(lambda: shape.move_right(grid), "Right")
wn.onkeypress(lambda: shape.move_left(grid), "Left")
wn.onkeypress(lambda: speed_up(delay), "Down")
wn.onkeypress(lambda: shape.rotate(grid), "space")


while True:
    end = 1
    wn.update()
    if shape.y == 23 - shape.height + 1:
        shape = Shape()
        check_grid(grid)
    elif shape.can_move(grid, 0):
        shape.erase_shape(grid)
        shape.y += 1
        shape.draw_shape(grid)
    else:
        for i in range(5, 5 + shape.width):
            if grid[1][i] != 0:
                draw_game_over(pen)
                end = 0
            else:
                shape = Shape()
                check_grid(grid)

    if end == 0:
        break

    draw_grid(pen, grid)
    score.draw_score(pen)

    time.sleep(delay)


# wn.mainloop()

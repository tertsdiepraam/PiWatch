import random

import itertools

from piwatch import *
import time

seconds_till_frame = 0.15
score = 0
time_prev_frame = time.time()
snake = []
rows = 13
columns = 20
box_size = 15
LEFT = 'left'
RIGHT = 'right'
UP = 'up'
DOWN = 'down'
direction = 'right'
snake_color = (255, 255, 255)
goal_color = (50, 50, 255)
board_color = (0, 0, 0)
running = True
goal = None


def define_app():
    app = App(
        name='Snake',
        icon='icon.png'
    )

    main = Activity(
        name='main'
    )

    box_attrs = dict(
        Text.attributes,
        message='',
        size=1,
        fixed_size=box_size,
        bg_color=board_color,
    )

    board = Grid(
        children=[[Text(box_attrs) for _ in range(columns)] for _ in range(rows)],
        spacing=1,
        position=('center', 0, 10),
        bg_color=(30, 30, 30)
    )

    score_text = Text(
        size=20,
        font='impact',
        position=('center', 0, -40),
        message='score: 0'
    )

    game_over = Text(
        size=40,
        font='impact',
        message='Game Over!'
    )

    try_again = Text(
        size=25,
        font='impact',
        message='Try Again',
        padding=10,
        bg_color=(0, 0, 255),
        color=Color.WHITE,
        position=('center', 0, 60)
    )

    def generate_goal():
        point = (random.randint(0, columns-1), random.randint(0, rows-1))
        while point in snake:
            point = (random.randint(0, columns-1), random.randint(0, rows-1))
        return point

    @app.event_listener('started app {}'.format(app.name))
    def reset(event):
        global snake, time_prev_frame, running, direction, score, goal
        running = True
        direction = RIGHT
        score = 0
        time_prev_frame = time.time()
        if snake:
            for x, y in snake:
                board.children[y][x].update(bg_color=board_color)
        if goal:
            board.children[goal[1]][goal[0]].update(bg_color=board_color)
        snake = [(int(columns/2)-1, int(rows/2)), (int(columns/2), int(rows/2))]
        for x, y in snake:
            board.children[y][x].update(bg_color=snake_color)
        goal = generate_goal()
        board.children[goal[1]][goal[0]].update(bg_color=goal_color)
        board.update()
        game_over.update(visible=False)
        try_again.update(visible=False)
        score_text.update(visible=False)

    @app.event_listener('new frame')
    def frame(event):
        global time_prev_frame, running, goal, score
        if running and time.time() - time_prev_frame >= seconds_till_frame:

            # Calculate which box has to be added to the snake
            if direction == LEFT:
                new = (snake[-1][0] - 1, snake[-1][1])
            elif direction == RIGHT:
                new = (snake[-1][0] + 1, snake[-1][1])
            elif direction == UP:
                new = (snake[-1][0], snake[-1][1] - 1)
            elif direction == DOWN:
                new = (snake[-1][0], snake[-1][1] + 1)
            else:
                raise AttributeError("Direction must be 'left', 'right', 'up' or 'down'. It was {}".format(direction))

            # Check whether snake touches a green box. If so, the snake will grow
            if new == goal:
                board.children[goal[1]][goal[0]].update(bg_color=board_color)
                goal = generate_goal()
                board.children[goal[1]][goal[0]].update(bg_color=goal_color)
                score += 1
            else:
                last = snake.pop(0)
                board.children[last[1]][last[0]].update(bg_color=board_color)

            # Check game over conditions
            if new[0] < 0 or new[0] >= columns or new[1] < 0 or new[1] >= rows or new in snake:
                running = False
                game_over.update(visible=True)
                try_again.update(visible=True)
                score_text.update(
                    message='score: {}'.format(score),
                    visible=True)
            else:
                snake.append(new)
                board.children[new[1]][new[0]].update(bg_color=snake_color)
                time_prev_frame = time.time()
            board.update()

    @app.event_listener('mouse down')
    def mouse_down(event):
        if try_again.visible and try_again.check_collision(event.pos):
            reset(event)
        elif running:
            global direction
            x = event.pos[0]
            y_1 = 0.75 * x
            y_2 = -0.75 * x + 240
            if x < 160:
                # left side of the screen
                if event.pos[1] <= y_1:
                    direction = UP
                elif event.pos[1] >= y_2:
                    direction = DOWN
                else:
                    direction = LEFT
            else:
                # right side of the screen
                if event.pos[1] <= y_2:
                    direction = UP
                elif event.pos[1] >= y_1:
                    direction = DOWN
                else:
                    direction = RIGHT

    main.add(board, game_over, try_again, score_text)
    app.add(main)
    return app

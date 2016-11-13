from piwatch import *
import time

seconds_till_frame = 0.75
time_prev_frame = time.time()
snake = []
rows = 13
columns = 20
box_size = 14
direction = 'left'
snake_color = (255, 0, 0)
board_color = (50, 50, 50)
running = True

def define_app():
    app = App(
        name='Snake'
    )

    main = Activity(
        name='main'
    )

    box_attrs = dict(
        Text.attributes,
        message='',
        size=1,
        fixed_size=box_size,
        bg_color=board_color
    )

    board = Grid(
        children=[[Text(box_attrs) for box in range(columns)] for row in range(rows)],
        spacing=2,
        position=('center', 0, 10)
    )

    @app.event_listener('started app {}'.format(app.name))
    def boot(event):
        global snake, time_prev_frame
        time_prev_frame = time.time()
        snake = [(int(columns/2), int(rows/2)), (int(columns/2)+1, int(rows/2))]
        for x, y in snake:
            board.children[y][x].update(bg_color=snake_color)
        board.update()

    @app.event_listener('new frame')
    def frame(event):
        global time_prev_frame
        if running and time.time() - time_prev_frame >= seconds_till_frame:
            last = snake.pop(0)
            board.children[last[1]][last[0]].update(bg_color=board_color)
            if direction == 'left':
                new = (snake[-1][0] - 1, snake[-1][1])
                snake.append(new)
            elif direction == 'right':
                new = (snake[-1][0] + 1, snake[-1][1])
            elif direction == 'up':
                new = (snake[-1][0], snake[-1][1] - 1)
            elif direction == 'down':
                new = (snake[-1][0], snake[-1][1] + 1)
            else:
                raise AttributeError
            snake.append(new)
            board.children[new[1]][new[0]].update(bg_color=snake_color)
            board.update()
            time_prev_frame = time.time()

    main.add(board)
    app.add(main)
    return app
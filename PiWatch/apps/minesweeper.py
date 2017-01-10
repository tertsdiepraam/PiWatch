from piwatch import *
import random

running = False
rows = 10
columns = 7
amount_of_mines = 15
exclude_position = None


def define_app():
    app = App(
        name='Minesweeper',
        icon="icon.png"
    )

    main = Activity(
        name='main'
    )

    field_attrs = dict(
        Text.attributes,
        message='',
        bg_color=(200, 200, 210),
        fixed_size=28
    )

    board = Grid(
        spacing=3,
        position=('midbottom', 0, -3)
    )

    victory = Text(
        message='VICTORY',
        font='impact',
        size=70,
        color=(255, 255, 0)
    )

    start_again = Text(
        message='click to start again',
        size=20,
        color=Color.WHITE
    )

    vic_text = List(
        children=[victory, start_again],
        direction='down',
        bg_color=(0, 0, 0, 200),
        padding=(200, 10),
        visible=False,
        spacing=15,
    )

    def generate_grid(size_x, size_y, num_mines, exclude_pos=None):
        """Creates a grid of mines and numbers in fields indicating the number of mines around them.
            -1 = mine
            0-8 = no mine"""
        all_possible_positions = ((iii, jjj) for jjj in range(size_x) for iii in range(size_y))
        mine_positions = random.sample(list(filter(lambda pos: pos != tuple(reversed(exclude_pos)), all_possible_positions)), num_mines)
        grid = []
        for row_num in range(size_x):
            row = []
            for column_num in range(size_y):
                if (column_num, row_num) in mine_positions:
                    # -1 is a mine
                    row.append(-1)
                else:
                    row.append(0)
            grid.append(row)
        for row in range(size_x):
            for column in range(size_y):
                if (column, row) not in mine_positions:
                    neighbours = 0
                    for iii in [-1, 0, 1]:
                        for jjj in [-1, 0, 1]:
                            neighbours += 1 if (column + iii, row + jjj) in mine_positions else 0
                    grid[row][column] = neighbours
        return grid

    @app.event_listener('mouse up')
    def mouse_down(event):
        global running, exclude_position
        if not running:
            exit_loop = False
            for index_1, row in enumerate(board.children):
                for index_2, field in enumerate(row):
                    if field.check_collision(event.pos):
                        exclude_position = (index_1, index_2)
                        exit_loop = True
                        break
                if exit_loop:
                    break
            if not exit_loop:
                return
            num_grid = generate_grid(columns, rows, amount_of_mines, exclude_position)
            grid = []
            for num_row in num_grid:
                row = []
                for num_field in num_row:
                    field = Text(
                        field_attrs,
                        num=num_field,
                        uncovered=False
                    )
                    row.append(field)
                grid.append(row)
            board.clear()
            board.add(*grid)
            excluded_field = board.children[exclude_position[0]][exclude_position[1]]
            if excluded_field.num == 0:
                excluded_field.update(
                    bg_color=Color.BLACK,
                    uncovered=True
                )
            else:
                excluded_field.update(
                    message=str(excluded_field.num),
                    bg_color=Color.BLACK,
                    uncovered=True
                )
            board.update()
            running = True
            vic_text.update(visible=True)
        else:
            for field in filter(lambda x: x.message == '', board.flat_children):
                if field.check_collision(event.pos):
                    if field.num == -1:
                        field.update(
                            message='X',
                            bg_color=Color.RED)
                        running = False
                        break
                    elif field.num == 0:
                        field.update(
                            bg_color=Color.BLACK,
                            uncovered=True
                        )
                    else:
                        field.update(
                            message=str(field.num),
                            bg_color=Color.BLACK,
                            uncovered=True)
                    print(len(list(board.flat_children)))
                    print(rows*columns - len(list(filter(lambda x: x.uncovered, board.flat_children))))
                    if len(list(board.flat_children)) - len(list(filter(lambda x: x.uncovered, board.flat_children))) == amount_of_mines:
                        running = False
                        vic_text.update(visible=True)
                    break
            board.update()

    board.children = []
    board.add(*[[Text(field_attrs, num=0) for _ in range(rows)] for _ in range(columns)])

    main.add(board, vic_text)
    app.add(main)
    return app

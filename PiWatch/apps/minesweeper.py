from piwatch import *
import random


def define_app():
    app = App(
        name='Minesweeper'
    )

    main = Activity(
        name='main'
    )

    field_attrs = dict(
        Text.attributes,
        message='',
        bg_color=Color.GREY,
        fixed_size=28
    )

    board = Grid(
        spacing=3,
        position=('midbottom', 0, -3)
    )

    def generate_grid(size_x, size_y):
        """Creates a grid of mines and numbers in fields indicating the number of mines around them.
            -1 = mine
            0-8 = no mine"""
        num_mines = 20
        mine_positions = random.sample([(iii, jjj) for jjj in range(size_x) for iii in range(size_y)], num_mines)
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

    @app.event_listener('started app {}'.format(app.name))
    def boot(event):
        global running
        running = True
        rows = 10
        columns = 7
        num_grid = generate_grid(columns, rows)
        grid = []
        for num_row in num_grid:
            row = []
            for num_field in num_row:
                field = Text(
                    field_attrs,
                    num=num_field
                )
                row.append(field)
            grid.append(row)
        board.clear()
        board.add(*grid)

    @app.event_listener('mouse down')
    def mouse_down(event):
        global running
        for field in filter(lambda field: field.message == '', board.flat_children):
            if field.check_collision(event.pos):
                if field.num == -1:
                    field.update(message='X')
                    running = False
                else:
                    field.update(message=str(field.num))
                break
        board.update()

    main.add(board)
    app.add(main)
    return app

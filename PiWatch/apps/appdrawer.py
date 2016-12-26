from piwatch import *
import copy


def define_app():
    app = App(
        name='appdrawer'
    )

    main = Activity(
        name='main'
    )

    grid = Grid(
        List.attributes,
        children=[],
        direction='down',
        alignment='midtop',
        padding=5,
        position=('center', 0, 0)
    )

    itemattrs = dict(
        List.attributes,
        direction='down',
        alignment='midtop',
        spacing=3,
        padding=3
    )

    iconattrs = dict(
        Image.attributes,
        size_x=32,
        size_y=32
    )

    textattrs = dict(
        Text.attributes,
        size=15
    )

    @app.event_listener('started app ' + app.name)
    def start(event):
        app.global_eventqueue.add(Event('main get variable', data='apps'))

    @app.event_listener('variable return')
    def got_apps(event):
        rowsize = 3
        apps = sorted(filter(lambda x: x.name != 'appdrawer', list(event.data[1].values())), key=lambda x: x.name)
        rows = (apps[x:x+rowsize] for x in range(0, len(apps), rowsize))
        rows_in_grid = []
        for row in rows:
            items_in_row = []
            for _app in row:
                if _app.icon:
                    icon = Image(
                        iconattrs,
                        filename=_app.folder + _app.icon
                    )
                else:
                    icon = Image(
                        iconattrs,
                        filename=app.folder + "missing_icon.png"
                    )
                if _app.name:
                    title = Text(
                        textattrs,
                        message=_app.name
                    )
                else:
                    title = Text(
                        textattrs,
                        message='No Name'
                    )
                item = List(
                    itemattrs,
                    children=[icon, title],
                    app_to_start=_app.name,
                )
                items_in_row.append(item)
            rows_in_grid.append(copy.deepcopy(items_in_row))
        grid.clear()
        grid.add(*rows_in_grid)

    @app.event_listener('mouse up')
    def mouse_up(event):
        for row in grid.children:
            for item in row:
                if item.check_collision(event.pos):
                    app_name = item.children[1].message
                    app.global_eventqueue.add('main start app', data=app_name)

    main.add(grid)
    app.add(main)
    return app

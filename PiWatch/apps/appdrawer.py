from piwatch import *


def define_app():
    app = App(
        name='appdrawer'
    )

    main = Activity(
        name='main'
    )

    grid = List(
        List.attributes,
        direction='right',
        alignment='topleft',
        padding=5,
        position=('center', 0, 0),
        id='grid'
    )
    rowattrs = dict(
        List.attributes,
        direction='right',
        alignment='topleft',
        padding=5
    )

    itemattrs = dict(
        List.attributes,
        direction='down',
        alignment='midtop',
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

    rowsize = 1

    @app.event_listener('start app ' + app.name)
    def start(event):
        app.global_eventqueue.add(Event('main get variable', data='apps'))

    @app.event_listener('variable return')
    def got_apps(event):
        apps = list(event.data[1].values())
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
                items_in_row.append(EvenlySpacedList(
                    itemattrs,
                    children=[icon, title]
                ))
            rows_in_grid.append(EvenlySpacedList(
                rowattrs,
                children=items_in_row
            ))
        grid.clear()
        grid.add(*rows_in_grid)

    main.add(grid)
    app.add(main)
    return app

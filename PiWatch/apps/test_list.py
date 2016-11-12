from piwatch import *


def define_app():
    app = App(
        name='list test'
    )
    main = Activity(
        name='main'
    )
    listy = List(
        children=[
            Text(message='333'),
            Text(message='22'),
            Text(message='1')
        ],
        direction='down',
        padding=5
    )
    main.add(listy)
    app.add(main)
    return app

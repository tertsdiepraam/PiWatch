from piwatch import *


def define_app():
    app = App(
        name='Waterproof'
    )

    main = Activity(
        name='main'
    )

    instruction_attrs = dict(
        Text.attributes,
        size=20,
        color=(0, 0, 0)
    )

    instruction_1 = Text(
        instruction_attrs,
        message='Keep the device under water.'
    )

    instruction_2 = Text(
        instruction_attrs,
        message='Touch "BEGIN TEST" to start.'
    )

    instructions = List(
        direction='down',
        padding=20,
        alignment='center',
        children=[instruction_1, instruction_2],
        position=('midtop', 0, 50),
        bg_color=(255, 255, 255, 150),
        spacing=5
    )

    bttn = Text(
        message='BEGIN TEST',
        color=(0, 0, 0),
        position=('midbottom', 0, -30),
        bg_color=(255, 255, 255, 150),
        size=30,
        padding=20
    )

    background_image = Image(
        filename=app.folder + 'background.png',
    )

    @app.event_listener('started app {}'.format(app.name))
    def startup(event):
        instruction_1.update(message='Keep the device under water.')
        instruction_2.update(message='Touch "BEGIN TEST" to start.')
        instructions.update()
        bttn.update(color=(0, 0, 0),
                    bg_color=(255, 255, 255, 150))

    @app.event_listener('mouse down')
    def click(event):
        if bttn.check_collision(event.pos):
            instruction_1.update(message='If you really kept it under water')
            instruction_2.update(message='your device is WATERPROOF!')
            instructions.update()
            bttn.update(color=(0, 0, 0, 150),
                        bg_color=(255, 255, 255, 50))

    main.add(background_image, instructions, bttn)
    app.add(main)
    return app
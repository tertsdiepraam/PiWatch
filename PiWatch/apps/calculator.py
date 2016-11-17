from piwatch import *

# variables
current_calc = ''
bttns = {}


def define_app():
    # declare the app
    app = App(
        name='Calculator',
        icon='background.png'
    )

    # declare the main activity
    main = Activity(
        name='main'
    )

    # visual components
    display_attrs = dict(
        Text.attributes,
        size=35,
        message=''
    )
    calculation_text = Text(
        display_attrs,
        position=('topleft', 10, 17)
    )
    answer_text = Text(
        display_attrs,
        position=('topright', -10, 53)
    )

    bttn_attrs = dict(
        Text.attributes,
        size=23,
        bg_color=(76, 106, 156),
        message='1',
        fixed_size=(56, 30)
    )

    bttn_grid = Grid(
        position=('midbottom', 0, -10),
        spacing=5,
        bg_color=(51, 71, 104),
        padding=10
    )

    # functions
    @app.event_listener('started app {}'.format(app.name))
    def boot(event):
        char_list = ['789+<',
                     '456-C',
                     '123*.',
                     '0()/=']
        grid = []
        for string in char_list:
            row = []
            for char in string:
                bttn = Text(
                    bttn_attrs,
                    message=char
                )
                bttns[bttn] = char
                row.append(bttn)
            grid.append(row)
        bttn_grid.clear()
        bttn_grid.add(*grid)

    @app.event_listener('mouse up')
    def mouse_down(event):
        global current_calc
        answer = ''
        for button in bttns.keys():
            if button.check_collision(event.pos):
                char = bttns[button]
                if char == '<':
                    current_calc = current_calc[:-1]
                elif char == 'C':
                    current_calc = ''
                elif char == '=':
                    pass
                else:
                    current_calc += char
                if len(current_calc) > 14:
                    calc_text = '...' + current_calc[int(len(current_calc)/14)*14-1:]
                else:
                    calc_text = current_calc
                calculation_text.update(message=calc_text)
                try:
                    answer = eval(current_calc)
                    if type(answer) is float:
                        if answer % 1 == 0:
                            answer = int(answer)
                        else:
                            answer = round(answer, 10)
                except SyntaxError:
                    pass
                except ZeroDivisionError:
                    answer = 'division by zero'
                answer_text.update(message=str(answer))

    main.add(calculation_text, answer_text, bttn_grid)
    app.add(main)
    return app
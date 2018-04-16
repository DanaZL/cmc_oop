import os

import toga
from toga.constants import COLUMN, ROW
from toga.style.pack import *

label_style = Pack(flex=1, padding_right=24)
box_style = Pack(direction=ROW, padding=10)
slider_style = Pack(flex=1)

def button_handler(widget):
    print('button handler')
    for i in range(0, 10):
        print("hello", i)
        yield 1
    print("done", i)


def action0(widget):
    print("action 0")


def action1(widget):
    print("action 1")


def action2(widget):
    print("action 2")


def action3(widget):
    print("action 3")

def action4(widget):
    print("CALLING Action 4")
    cmd3.enabled = not cmd3.enabled

class SecretaryApp(toga.App):
    def icon_init(self):
        path = os.path.dirname(os.path.abspath(__file__))
        self.brutus_icon = os.path.join(path, "icons", "brutus.icns")
        self.cricket_icon = os.path.join(path, "icons", "cricket-72.png")
        self.step_icon = os.path.join(path, "")

    def build_schedule(self):
        tree = toga.Tree(['Schedule'], )
        # print(dir(tree))
        tree.data.append(None, None, 'root1')
        root2 = tree.data.append(None, None, 'root2')
        tree.data.append(root2, None, 'root2.1')
        root2_2 = tree.data.append(root2, None, 'root2.2')
        tree.data.append(root2_2, None, 'root2.2.1')
        tree.data.append(root2_2, None, 'root2.2.2')
        tree.data.append(root2_2, None, 'root2.2.3')
        return tree

    def build_settings(self):
        settings_box = toga.Box(
                children=[
                    toga.Box(style=box_style, children=[
                        toga.Label("Период моделирования",
                            style=label_style),
                        toga.Slider(range=(7, 31), default=14, style=Pack(width=100)),
                    ]),

                    toga.Box(style=box_style, children=[
                        toga.Label("Количество отделов",
                            style=label_style),

                        toga.Slider(range=(5, 10), default=7, style=Pack(width=100)),
                    ])
                ],
                style=Pack(direction=COLUMN, padding=24)
        )
        return settings_box

    def startup(self):
        self.icon_init()
        self.main_window = toga.MainWindow(title=self.name, size=(700, 500))

        tree = self.build_schedule()
        right_container = toga.ScrollContainer(horizontal=False)

        # right_container.content = right_content
        right_container.content = self.build_settings()

        split = toga.SplitContainer()

        split.content = [tree, right_container]

        self.main_window.content = split

        things = toga.Group('Things')

        cmd0 = toga.Command(
            action1,
            label='Action 0',
            tooltip='Perform action 0',
            icon=self.brutus_icon,
            group=things
        )
        cmd1 = toga.Command(
            action1,
            label='Action 1',
            tooltip='Perform action 1',
            icon=self.brutus_icon,
            group=things
        )
        cmd2 = toga.Command(
            action2,
            label='Action 2',
            tooltip='Perform action 2',
            icon=toga.Icon.TIBERIUS_ICON,
            group=things
        )
        cmd3 = toga.Command(
            action3,
            label='Action 3',
            tooltip='Perform action 3',
            shortcut='k',
            icon=self.cricket_icon
        )

        cmd4 = toga.Command(
            action4,
            label='Action 4',
            tooltip='Perform action 4',
            icon=self.brutus_icon
        )

        self.main_window.show()


def main():
    return SecretaryApp('Secretary', '42')

if __name__ == '__main__':
    main().main_loop()
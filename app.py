import os

import toga
from toga.constants import COLUMN, ROW
from toga.style.pack import *
from experiment import Experiment
from secretary import Secretary

label_style = Pack(flex=1, padding_right=24)
box_style = Pack(direction=ROW, padding=5)
slider_style = Pack(flex=1)
schedule_style= Pack(flex=1, width=450)

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
    def start_experiment(self, widget):
        self.exp_duration.enabled = False
        self.cnt_department.enabled = False
        self.experiment = Experiment(int(self.cnt_department.value),
                                    int(self.exp_duration.value))
        schedule = self.experiment.start_experiment()
        print(schedule)
        self.build_table(schedule)


    def icon_init(self):
        path = os.path.dirname(os.path.abspath(__file__))
        self.brutus_icon = os.path.join(path, "icons", "brutus.icns")
        self.cricket_icon = os.path.join(path, "icons", "cricket-72.png")
        self.step_icon = os.path.join(path, "")

    def build_schedule(self):
        self.tree = toga.Tree(['Номер события', 'Название события', 'Помещение', 'Периодичность', 'Участники'],
                        style=schedule_style)
        # print(dir(tree))
        self.tree.data.append(None, None, None, None,  None,'root1')
        root2 = self.tree.data.append(None, None,None, None, None, 'root2')
        self.tree.data.append(root2, None, None, None, None, 'root2.1')
        root2_2 = self.tree.data.append(root2, None, None, None, None,'root2.2')
        self.tree.data.append(root2_2, None, None, None, None, 'root2.2.1')
        self.tree.data.append(root2_2, None, None, None, None, 'root2.2.2')
        self.tree.data.append(root2_2, None, None, None, None, 'root2.2.3')
        return self.tree

    def build_table(self, schedule):
        self.tree.refresh()
        self.tree = toga.Tree(['Время', 'Номер события', 'Название события',\
                          'Помещение', 'Периодичность', 'Участники'],
                        style=schedule_style)

        for event in schedule:
            description = event.get_description()
            event_row = self.tree.data.append(None, description[0], str(event.event_id),
                            event.name, str(event.room), description[1], 
                            "...")
            for worker in event.participants:
                self.tree.data.append(event_row, "", "", "", "", "", worker)
        print(self.tree)
        # return self.tree


    def build_settings(self):
        self.exp_duration = toga.Selection(items=[str(i) for i in range(7, 32)])
        self.cnt_department = toga.Selection(items=[str(i) for i in range(5, 10)])
        progress = toga.ProgressBar(max=100, value=1, style=Pack(padding_top=20))

        settings_box = toga.Box(
                children=[
                    toga.Box(style=box_style, children=[
                        toga.Label("Период моделирования",
                            style=label_style),
                        self.exp_duration
                    ]),

                    toga.Box(style=box_style, children=[
                        toga.Label("Количество отделов",
                            style=label_style),
                        self.cnt_department
                    ]),

                    toga.Box(style=box_style, children=[
                        toga.Label("Шаг моделирования",
                            style=label_style),
                        self.cnt_department
                    ]),
                    toga.Button('Начать моделирование', on_press=self.start_experiment, 
                                style=Pack(flex=1, width=250, alignment='right')),
                    progress
                ],
                style=Pack(direction=COLUMN, padding=24)
        )
        return settings_box

    def startup(self):
        self.icon_init()
        self.main_window = toga.MainWindow(title=self.name, size=(1500, 900))

        self.tree = self.build_schedule()
        self.tree.refresh()
        right_container = toga.ScrollContainer(horizontal=False)

        # right_container.content = right_content
        right_container.content = self.build_settings()

        split = toga.SplitContainer()
        split.content = [self.tree, right_container]

        print(self.tree)
        # split = toga.Box(style=box_style, children=[tree, right_container]) 

        self.main_window.content = split
        self.main_window.show()


def main():
    return SecretaryApp('Secretary', '42')

if __name__ == '__main__':
    main().main_loop()
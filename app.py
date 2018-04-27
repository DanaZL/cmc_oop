import os

import toga
from toga.constants import COLUMN, ROW, BOLD
from toga.style.pack import *
from experiment import Experiment
from secretary import Secretary

label_style = Pack(flex=1, padding_right=24)
box_style = Pack(direction=ROW, padding=5)
slider_style = Pack(flex=1)
schedule_style= Pack(flex=1, width=450)
main_label_style = Pack(flex=1, padding_right=24)


class SecretaryApp(toga.App):

    def start_experiment(self, widget):
        self.exp_duration.enabled = False
        self.cnt_department.enabled = False

        self.experiment = Experiment(cnt_department=int(self.cnt_department.value),
                                    exp_period=int(self.exp_duration.value))

        schedule = self.experiment.start_experiment()
        # print(schedule)
        self.build_table(schedule)


    def step(self, widget):
        schedule, curtime = self.experiment.step(int(self.exp_step.value.split()[0]))
        print(dir(self.label_curtime))
        self.label_curtime.text = "Текущее время: {} день {}.00".format(curtime[0], curtime[1])
        self.build_table(schedule)


    def icon_init(self):
        path = os.path.dirname(os.path.abspath(__file__))
        self.brutus_icon = os.path.join(path, "icons", "brutus.icns")
        self.cricket_icon = os.path.join(path, "icons", "cricket-72.png")
        self.step_icon = os.path.join(path, "")


    def build_schedule(self):
        self.tree = toga.Tree(['Время (День/Часы)', 'Номер события', 'Название события', 'Помещение', 'Периодичность', 'Участники'],
                        style=schedule_style)
        return self.tree


    def build_table(self, schedule):
        for node in self.tree.data[::-1]:
            self.tree.data.remove(node)

        for event in schedule:
            print (event.start_time, event.duration)
            description = event.get_description()
            event_row = self.tree.data.append(None, description['date'], str(event.event_id),
                            event.name, description['room'], description['freq'], 
                            "...\n")
            for worker in event.participants:
                self.tree.data.append(event_row, "", "", "", "", "", worker)
        print(self.tree)
        # return self.tree


    def build_settings(self):
        self.exp_duration = toga.Selection(items=[str(i) for i in range(7, 32)])
        self.cnt_department = toga.Selection(items=[str(i) for i in range(5, 10)])
        self.exp_step = toga.Selection(items=[str(i) + " час" for i in range(1, 10)])

        self.btn_start_experiment = toga.Button('Начать моделирование', on_press=self.start_experiment, 
                                style=Pack(flex=1, width=250, alignment='right'))

        self.btn_step = toga.Button('Выполнить шаг моделирования', on_press=self.step, 
                                style=Pack(flex=1, width=300, height=38))

        self.label_curtime = toga.Label("Текущее время: 0 день 0.00", style=main_label_style)

        progress = toga.ProgressBar(max=100, value=1, style=Pack(padding_top=15))

        self.settings_box = toga.Box(
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

                    self.btn_start_experiment,
                    progress
                ],
                style=Pack(direction=COLUMN, padding=24)
        )

        self.step_box = toga.Box(
                children=[
                    toga.Box(
                        children=[
                            self.label_curtime

                    ]),
                    toga.Box(
                        children=[
                        toga.Label("Шаг моделирования",
                            style=label_style),
                        self.exp_step, 
                        self.btn_step
                    ],
                    style=Pack(direction=ROW, padding=14))
                ],
                style=Pack(direction=COLUMN, padding=24)
        )   

        self.content_box = toga.Box(
                children=[self.settings_box, self.step_box],
                style=Pack(direction=COLUMN)
        )

        return self.content_box


    def startup(self):
        self.icon_init()
        self.main_window = toga.MainWindow(title=self.name, size=(1800, 800))

        self.tree = self.build_schedule()
        # self.tree.refresh()
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
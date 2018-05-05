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
table_style= Pack(flex=1, width=150, height=150)
main_label_style = Pack(flex=1, padding_right=24)


class SecretaryApp(toga.App):

    def start_experiment(self, widget):
        self.exp_duration.enabled = False
        self.cnt_department.enabled = False

        self.experiment = Experiment(cnt_department=int(self.cnt_department.value),
                                    exp_period=int(self.exp_duration.value))


        for dep in self.experiment.departments:
            for w in dep.workers:
                self.add_event_participants_list.data.append(w)
            self.add_event_participants_list.data.append(dep.boss)    
        schedule = self.experiment.start_experiment()
        print(self.add_event_participants_list.multiple_select)

        self.build_table(schedule)


    def step(self, widget):
        schedule, curtime = self.experiment.step(int(self.exp_step.value.split()[0]))
        print(dir(self.label_curtime))
        self.label_curtime.text = "Текущее время: {} день {}.00".format(curtime[0], curtime[1])
        self.build_table(schedule)

    def add_event(self, widget):
        participants = [p for p in self.add_event_participants.value.split(",")]
        schedule, warning = self.experiment.add_event(int(self.add_event_day.value),
                                                      int(self.add_event_time.value),
                                                      int(self.add_event_duration.value),
                                                      int(self.add_event_room.value),
                                                      self.add_event_name.value,
                                                      participants,
                                                      )
        if warning != "":
            self.label_warning.text = "WARNING! \n" + warning
        self.build_table(schedule)

    def delete_event(self, widget):
        schedule, warning = self.experiment.delete_event(int(self.delete_event_id.value))
        if warning != "":
            self.label_warning.text = "WARNING! \n" + warning
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

        self.select_event_day = toga.Selection(items=[str(i) for i in range(0, 32)])
        self.select_event_hour = toga.Selection(items=[str(i) for i in range(5, 10)])

        self.btn_start_experiment = toga.Button('Начать моделирование',
                                            on_press=self.start_experiment, 
                                            style=Pack(flex=1, width=250, alignment='right'))

        self.btn_step = toga.Button('Выполнить шаг моделирования', on_press=self.step, 
                                style=Pack(flex=1, width=300, height=38))

        self.btn_add_event = toga.Button('Добавить событие', on_press=self.add_event, 
                                style=Pack(flex=1, width=300, height=38))

        self.add_event_day = toga.Selection(items=[str(i) for i in range(32)])
        self.add_event_time = toga.Selection(items=[str(i) for i in range(24)])
        self.add_event_duration = toga.Selection(items=[str(i) for i in range(24)])
        self.add_event_room = toga.Selection(items=[str(1 + i) for i in range(5)])
        self.add_event_name = toga.TextInput(placeholder='Название события')

        self.add_event_participants_list = toga.Table(['Имя работника'],
                                                multiple_select=True,
                                                style=table_style)
        self.add_event_participants = toga.TextInput(placeholder='Участники через запятую',
                                                    style=Pack(width=200))


        self.btn_delete_event = toga.Button('Удалить событие', on_press=self.delete_event, 
                                style=Pack(flex=1, width=300, height=38))
        self.delete_event_id = toga.Selection(items=[str(i) for i in range(100)])

        self.label_curtime = toga.Label("Текущее время: 0 день 0.00", style=main_label_style)

        self.label_warning = toga.Label("", style=main_label_style)


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
                    progress,
                    self.label_warning,
                ],
                style=Pack(direction=COLUMN, padding=24)
        )

        self.step_box = toga.Box(
                children=[
                    toga.Box(
                        children=[
                            self.label_curtime,
                            
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

        self.add_event_box = toga.Box(
                children = [
                    toga.Box(style=box_style, children=[
                        toga.Label("День",
                            style=label_style),
                        self.add_event_day
                    ]),

                    toga.Box(style=box_style, children=[
                        toga.Label("Время",
                            style=label_style),
                        self.add_event_time
                    ]),

                    toga.Box(style=box_style, children=[
                        toga.Label("Длительность",
                            style=label_style),
                        self.add_event_duration
                    ]),

                    toga.Box(style=box_style, children=[
                        toga.Label("Комната",
                            style=label_style),
                        self.add_event_room
                    ]),

                    toga.Box(style=box_style, children=[
                        toga.Label("Название",
                            style=label_style),
                        self.add_event_name
                    ]),

                    toga.Box(style=box_style, children=[
                        toga.Label("Участники",
                            style=label_style),
                        self.add_event_participants_list,
                        self.add_event_participants
                    ]),

                    self.btn_add_event,
                    
                ],
                style=Pack(direction=COLUMN, padding=24)
            )

        self.delete_event_box = toga.Box(
                children = [
                    toga.Box(style=box_style, children=[
                        toga.Label("Номер события",
                            style=label_style),
                        self.delete_event_id
                    ]),
                    self.btn_delete_event,                    
                ],
                style=Pack(direction=COLUMN, padding=24)
            )   

        self.content_box = toga.Box(
                children=[self.settings_box,
                          self.step_box,
                          self.add_event_box,
                          self.delete_event_box],
                style=Pack(direction=COLUMN)
        )

        return self.content_box


    def startup(self):
        self.icon_init()
        self.main_window = toga.MainWindow(title=self.name, size=(1800, 1000))

        self.tree = self.build_schedule()
        # self.tree.refresh()
        right_container = toga.ScrollContainer()

        # right_container.content = right_content
        right_container.content = self.build_settings()

        split = toga.SplitContainer()
        split.content = [self.tree, right_container]


        self.main_window.content = split
        self.main_window.show()


def main():
    return SecretaryApp('Secretary', '42')

if __name__ == '__main__':
    main().main_loop()
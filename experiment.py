from tools import date_sum, is_date_intersection
import random
from copy import deepcopy
from secretary import Secretary


class Experiment():
    def __init__(self, cnt_department,
                exp_period):
        self.cnt_department = cnt_department
        self.experiment_period = exp_period
        self.departments = [Department(i +1) 
                            for i in range(self.cnt_department)]

    def start_experiment(self):
        self.secretary = Secretary(cnt_department=self.cnt_department,
                                    experiment_period=self.experiment_period,
                                    departments=self.departments)
        self.secretary.generate_init_events()
        return self.secretary.schedule


    def step(self, cnt_step=1):
        self.secretary.step(cnt_step)
        return self.secretary.schedule, self.secretary.cur_time

    def add_event(self, day, time, duration, room, name, participants):
        warning = self.secretary.add_event((day, time),
                                            duration=(duration // 24, duration % 24),
                                            room=room,
                                            participants=participants,
                                            priority=1,
                                            frequency=0,
                                            name=name)

        return self.secretary.schedule, warning 

    def delete_event(self, event_id):
        warning = self.secretary.delete_event(event_id)
        return self.secretary.schedule, warning

class Department():
    def __init__(self, dep_id):
        self.id = dep_id
        self.cnt_workers = random.choice(range(7))
        self.workers = [str(self.id) + "." + str(i) for i in range(self.cnt_workers)]
        self.boss = str(self.id) + ".boss"
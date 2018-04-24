from tools import date_sum, is_date_intersetction
from generators import initial_events
import random as r
from copy import deepcopy


class Experiment():
    def __init__(self, cnt_department,
                exp_period):
        self.cnt_department = cnt_department
        self.experiment_period = exp_period
        self.departments = [Department(i +1) 
                            for i in range(self.cnt_department)]

    def start_experiment(self):
        self.secretary = Secretary(self.cnt_department)
        self.secretary.generate_init_events()

    def step(self, cnt_step=1):
        self.secretary.step(cnt_step)


class Department():
    def __init__(self, dep_id):
        self.id = dep_id
        self.cnt_workers = r.choice(range(7))
        self.workers = [str(self.id) + "." + i for i in range(cnt_workers)]
        self.boss = str(self.id) + ".boss"
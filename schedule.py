from tools import date_sum
from generators import initial_events
import random as r

class Department():
    def __init__(self, dep_id):
        self.id = dep_id
        self.cnt_workers = r.choice(range(7))
        self.workers = [str(self.id) + "." + i for i in range(cnt_workers)]
        self.boss = str(self.id) + ".boss"

class Event():
    def __init__(self,
                 start_time,
                 duration,
                 room,
                 participants,
                 priority,
                 name,
                 event_id):
        self.star_time = start_time
        self.duration = duration
        self.end_time = date_sum(start_time, duration)

        self.room = room
        self.participants = participants
        self.priority = priority
        self.name = name
        self.event_id = event_id


class Experiment():
    def __init__(self, cnt_department,
                exp_period):
        self.cnt_department = cnt_department
        self.experiment_period = exp_period
        self.departments = [Department(i + 1) 
                            for i in range(self.cnt_department)]

    def start_experiment(self):
        self.secretary = Secretary(self.cnt_department)
        self.secretary.generate_init_events()


class Secretary():
    def __init__(self, cnt_department, departments):
        #time: pair: (day, hour)
        self.cur_time = (0, 0)
        self.uniq_events = []
        self.event_ids = set()
        self.cnt_department = cnt_department
        self.departments = departments

    def calculate_schedule(self):
        self.schedule = []
        pass

    def add_event(self, 
                  start_time,
                  duration,
                  room,
                  participants,
                  priority,
                  period,
                  name):
        for i in range(max(self.event_ids) + 2):
            if i not in self.event_ids:
                event_id = i
                self.event_ids.add(i)
                break
        new_event = Event(start_time, duration,
                        room, participants,
                        priority, name)

    def generate_init_events(self):
        meeting_time = [r.choice(range(24)) for i in range(self.cnt_department)]
        for i in range(self.cnt_department):
            #одночасовые ежедневные планерки всех отделов
            self.add_event((-1, meeting_time), 
                            duration=1,
                            room=i, 
                            participants=self.departments[i].workers + [self.departments[i].boss],
                            priority=1,
                            name="Ежедневная планерка отдела " + self.departments[i].id)

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
                 frequency,
                 event_id):
        """
        Одноразовое - 0; Ежедневное - 1; Еженедельное - 2 
        """
        self.start_time = start_time
        self.duration = duration
        self.end_time = date_sum(start_time, duration)

        self.room = room
        self.participants = participants
        self.priority = priority
        self.name = name
        self.event_id = event_id


    def deploy_frequency(self, experiment_period):
        """
        Разворачиваем событие с учетом периодичности
        """
        events = []
        if self.frequency == 0:
            return [self]
        if self.frequency == 1:
            for day in range(experiment_period):
                new_event = deepcopy(self)
                new_event.start_time = (day, new_event.start_time[1])
                events.append(new_event)
        if self.frequency == 2:
            for day in range(0, experiment_period, 7):
                new_event = deepcopy(self)
                new_event.start_time = (day, new_event.start_time[1])
                events.append(new_event)

        return events



    def is_conflict(self, other_event):
        #TODO  добавить проверку на текущее время!!!
        if is_date_intersetction(self.start_time, self.duration,
                                other_event.start_time, other_event.duration):
            if self.room == other_event.room:
                return (True, 'room')
            if len(set(self.participants).intersection(other_event.participants)) > 0:
                return (True, 'participants')
        return False
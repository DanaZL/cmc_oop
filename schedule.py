from tools import date_sum

class Experiment():
    def __init__(self, cnt_department,
                exp_period):
        self.cnt_department = cnt_department
        self.experiment_period = exp_period

    def start_experiment(self):
        self.secretary = Secretary()



class Secretary():
    def __init__(self):
        #time: pair: (day, hour)
        self.cur_time = (0, 0)
        self.uniq_events = []
        self.event_ids = set()

    def calculate_schedule(self):
        self.schedule = []
        pass

    def add_event(self, start_time,
                        duration,
                        room,
                        participants,
                        priority,
                        name):
        for i in range(max(self.event_ids) + 2):
            if i not in self.event_ids:
                event_id = i
                self.event_ids.add(i)
                break
        new_event = Event(start_time, duration,
                        room, participants,
                        priority, name)

    def generate_begin_events(self):
        pass


class Event():
    def __init__(self,
                 start_time,
                 duration,
                 room,
                 participants,
                 priority,
                 name,
                 event_id
                 ):
        self.star_time = start_time
        self.duration = duration
        self.end_time = date_sum(start_time, duration)

        self.room = room
        self.participants = participants
        self.priority = priority
        self.name = name
        self.event_id = event_id




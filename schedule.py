
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



secretary = Secretary()

def Event():
    def __init__(self,
                 start_time,
                 duration,
                 room,
                 participants,
                 priority,
                 name,
                 ):

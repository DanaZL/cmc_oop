from tools import date_sum, date_compare
import operator
import random
from event import Event

class Secretary():
    def __init__(self, experiment_period, cnt_department, departments):
        #time: pair: (day, hour)
        self.cur_time = (0, 0)
        self.uniq_events = []
        #отсортированные по времени события
        self.schedule = []
        self.event_ids = set([0])
        self.cnt_department = cnt_department
        self.departments = departments
        self.experiment_period = experiment_period


    def step(self, cnt_step):
        self.cur_time = date_sum(self.cur_time, (0, self.cnt_step))
        for event_idx, event in enumerate(self.schedule):
            end_time = date_sum(event.start_time + event.duration)
            if date_compare(end_time, self.cur_time) < 0:
                self.schedule.pop(event_idx)


    def sort_schedule(self):
        self.schedule.sort(key=(lambda x: x.start_time[0] * 24 + x.start_time[1]))

    def check_conflicts(self, event):
        """
        Проверка на то, что добавляемое событие не конфликтует
        с событиями в календаре
        """
        for exist_event in self.schedule:
            is_conflict = exist_event.is_conflict(event)
            if not is_conflict:
                continue
            return (False, exist_event)
        return True


    def add_event(self, 
                  start_time,
                  duration,
                  room,
                  participants,
                  priority,
                  frequency,
                  name):

        
        new_event = Event(start_time=start_time,
                          duration=duration,
                          room=room,
                          participants=participants,
                          priority=priority,
                          frequency=frequency,
                          name=name)

        real_events = new_event.deploy_frequency(self.experiment_period,
                                                 self.cur_time)

        is_conflict = False
        for ev in real_events:
            conflict = self.check_conflicts(ev)
            if conflict == True:
                continue
            else:
              print ("Конфликт события {0} с событием {1}, уже существующем в календаре" %\
              format(str(ev), str(self))) 
              is_conflict = True
              break
        if not is_conflict:
            self.schedule.extend(real_events)

            for i in range(max(self.event_ids) + 2):
              if i not in self.event_ids:
                  event_id = i
                  self.event_ids.add(i)
                  break


    def generate_init_events(self):
        meeting_time = [random.choice(range(24)) for i in range(self.cnt_department)]
        print (meeting_time)
        for i in range(self.cnt_department):
            #одночасовые ежедневные планерки всех отделов
            self.add_event(start_time=(-1, meeting_time[i]), 
                            duration=(0, 1),
                            room=i, 
                            participants=self.departments[i].workers + [self.departments[i].boss],
                            priority=1,
                            frequency=1,
                            name="Ежедневная планерка отдела " + str(self.departments[i].id))

        self.sort_schedule()
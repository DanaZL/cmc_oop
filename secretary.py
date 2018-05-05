from tools import date_sum, date_compare
import operator
import random
from event import Event

class Secretary():
    def __init__(self, experiment_period, cnt_department, departments):
        #time: pair: (day, hour)
        self.cur_time = (0, 0)
        #отсортированные по времени события
        self.schedule = []
        self.event_ids = set([0])
        self.cnt_department = cnt_department
        self.departments = departments
        self.experiment_period = experiment_period


    def step(self, cnt_step):
        self.cur_time = date_sum(self.cur_time, (0, cnt_step))
        new_schedule = []
        for event_idx, event in enumerate(self.schedule):
            end_time = date_sum(event.start_time, event.duration)

            if date_compare(end_time, self.cur_time) < 0:
                new_schedule.append(event)
        self.schedule = new_schedule


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
        return True, None

    def delete_event(self, event_id):
      if event_id not in self.event_ids:
        return "События под номером {0} не существует в календаре".format(str(event_id))
      new_schedule = []
      for event in self.schedule:
          if event_id != event.event_id:
            new_schedule.append(event)

      self.event_ids.remove(event_id)
      self.schedule = new_schedule
      return ""


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

        if len(real_events) == 0:
            return "Попытка добавить событие в прошлом!"

        is_conflict = False
        for ev in real_events:
            conflict, exist_event = self.check_conflicts(ev)
            if conflict == True:
                continue
            else:
              return ("Конфликт события {0} с событием {1}, уже существующем в календаре".format(str(ev),
                                                                                         str(exist_event))) 
              is_conflict = True
              break

        if not is_conflict:
            for i in range(1000):
              if i not in self.event_ids:
                  for ev in real_events:
                      ev.event_id = i
                  self.event_ids.add(i)
                  break

            self.schedule.extend(real_events)
            self.sort_schedule()
        return ""



    def generate_init_events(self):
        meeting_time = [random.choice(range(24)) for i in range(self.cnt_department)]
        for i in range(self.cnt_department):
            #одночасовые ежедневные планерки всех отделов
            self.add_event(start_time=(-1, meeting_time[i]), 
                            duration=(0, 1),
                            room=i, 
                            participants=self.departments[i].workers + [self.departments[i].boss],
                            priority=1,
                            frequency=1,
                            name="Планерка отдела №" + str(self.departments[i].id))

        while True:
          boss_meeting_time = random.choice(range(24))
          boss_meeting_day = random.choice(range(7))
          if boss_meeting_time not in meeting_time:
              break

        self.add_event(start_time=(boss_meeting_day, boss_meeting_time), 
                      duration=(0, 1),
                      room=i, 
                      participants=[department.boss for department in self.departments],
                      priority=2,
                      frequency=2,
                      name="Совещание руководителей")
        print (len(self.schedule))

        self.sort_schedule()
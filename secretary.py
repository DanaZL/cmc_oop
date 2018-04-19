class Secretary():
    def __init__(self, experiment_period, cnt_department, departments):
        #time: pair: (day, hour)
        self.cur_time = (0, 0)
        self.uniq_events = []
        #отсортированные по времени события
        self.schedule = []
        self.event_ids = set()
        self.cnt_department = cnt_department
        self.departments = departments

    def calculate_schedule(self):
        self.schedule = []
        pass


    def check_conflicts(self, event):
        """
        Проверка на то, что добавляемое событие не конфликтует
        с событиями в календаре
        """
        for exist_event in self.schedule:
            is_conflict = exist_event.is_conflict(event)
            if not is_conflict:
                continue
            return (is_conflict[1], exist_event)
        return True


    def add_event(self, 
                  start_time,
                  duration,
                  room,
                  participants,
                  priority,
                  frequency,
                  name):
        for i in range(max(self.event_ids) + 2):
            if i not in self.event_ids:
                event_id = i
                self.event_ids.add(i)
                break
        new_event = Event(star_time=start_time,
                          duration=duration,
                          room=room,
                          participants=participants,
                          priority=priority,
                          frequency=frequency,
                          name=name)

        real_events = new_event.deploy_frequency()

        is_conflict = False
        for ev in real_events:



    def generate_init_events(self):
        meeting_time = [r.choice(range(24)) for i in range(self.cnt_department)]
        for i in range(self.cnt_department):
            #одночасовые ежедневные планерки всех отделов
            self.add_event((-1, meeting_time), 
                            duration=1,
                            room=i, 
                            participants=self.departments[i].workers + [self.departments[i].boss],
                            priority=1,
                            frequency=1,
                            name="Ежедневная планерка отдела " + self.departments[i].id)
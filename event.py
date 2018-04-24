from tools import date_compare


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
        frequency:
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


    def deploy_frequency(self, experiment_period, cur_time):
        """
        Разворачиваем событие с учетом периодичности
        """
        cur_day = cur_time[0]
        if self.start_time[1] < cur_time[0]:
            cur_day += 1

        events = []
        if self.frequency == 0 and date_compare(cur_time, self.start_time) >= 0:
            return [self]
        if self.frequency == 1:
            for day in range(cur_day, experiment_period):
                new_event = deepcopy(self)
                new_event.start_time = (day, new_event.start_time[1])
                events.append(new_event)
        if self.frequency == 2:
            for day in range(cur_day, experiment_period, 7):
                new_event = deepcopy(self)
                new_event.start_time = (day, new_event.start_time[1])
                events.append(new_event)

        return events


    def is_conflict(self, other_event):
        if is_date_intersetction(self.start_time, self.duration,
                                other_event.start_time, other_event.duration):
            if self.room == other_event.room:
                return (True, 'room')
            if len(set(self.participants).intersection(other_event.participants)) > 0:
                return (True, 'participants')
        return False


    def __str__(self):
        return self.name

    def get_description(self):
        end_time = date_sum(self.start_time, self.duration)
        date = "{}день {}.00 -\n {}день {}.00".format(str(self.start_time[0]),
                                              str(self.start_time[1]),
                                              str(self.end_time[0]),
                                              str(self.end_time[1]))

        # Одноразовое - 0; Ежедневное - 1; Еженедельное - 2
        if self.frequency == 0:
            freq = "-"
        elif self.frequency == 1:
            freq = "Ежедневное"
        else:
            freq = "Еженедельное"

        return [date, freq]
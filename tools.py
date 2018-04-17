def date_sum(date_1, date_2):
    hour = (date_1[1] + date_2[1]) % 24
    day = date_1[0] + date_2[0] + ((date_1[1] + date_2[1]) / 24)
    return (hour, day)
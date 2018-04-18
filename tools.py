def date_sum(date_1, date_2):
    hour = (date_1[1] + date_2[1]) % 24
    day = date_1[0] + date_2[0] + ((date_1[1] + date_2[1]) / 24)
    return (hour, day)

def is_date_intersect(strart_date_1, duration_1, start_date_2, duration_2):
	start_1 = date_1[0] * 24 + date_1[1]
	start_2 = date_2[0] * 24 + date_2[1]

	end_1 = start_1 + duration_1
	end_2 = start_2 + duration_2

	if start_1 > start_2 and start_1 > end_2:
		return False
	if start_1 < start_2 and end_1 < start_2:
		return False
	return True
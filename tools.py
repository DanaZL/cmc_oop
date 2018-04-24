def date_sum(date_1, date_2):
    hour = (date_1[1] + date_2[1]) % 24
    day = date_1[0] + date_2[0] + ((date_1[1] + date_2[1]) / 24)
    return (hour, day)

def date_compare(date_1, date_2):
	"""
	Сравнение двух дат:
	+1 - date_1 раньше date_2
	-1 - date_1 позже date_2
	0 - date_1  совпадает с date_2
	"""
	hour_1 = date_1[0] * 24 + date_1[1]
	hour_2 = date_2[0] * 24 + date_2[1]

	if hour_1 < hour_2:
		return 1
	elif hour_1 > hour_2:
		return -1:
	else:
		return 0


def is_date_intersection(strart_date_1, duration_1, start_date_2, duration_2):
	start_1 = date_1[0] * 24 + date_1[1]
	start_2 = date_2[0] * 24 + date_2[1]

	end_1 = start_1 + duration_1
	end_2 = start_2 + duration_2

	if start_1 > start_2 and start_1 > end_2:
		return False
	if start_1 < start_2 and end_1 < start_2:
		return False
	return True
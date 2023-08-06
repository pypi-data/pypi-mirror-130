from datetime import datetime

class Dublintime:
	date_1 = datetime.now()
	date_2 = '25/12/2021 11:13:08.230010'
	date_format_str = '%d/%m/%Y %H:%M:%S.%f'
	start = date_1
	end = datetime.strptime(date_2, date_format_str)
	# Get interval between two timstamps as timedelta object
	diff = end - start		# Get interval between two timstamps in hours
	diff_in_hours = diff.total_seconds() / 86400
	#return diff_in_hours()
	print('Difference is')
	print(float(diff_in_hours))

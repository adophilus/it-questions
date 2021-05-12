from datetime import datetime
import calendar

months = [
	"",
	"january",
	"february",
	"march",
	"april",
	"may",
	"june",
	"july",
	"august",
	"september",
	"october",
	"november",
	"december"
]

def getDateTime ():
	dt = datetime.now()
	return {
		"date": dt.strftime("%d"),
		"day": months[int(dt.strftime("%m"))],
		"month": months[int(dt.strftime("%m"))],
		"year": dt.strftime("%Y")
	}

def getCalendarArray ():
	present = datetime.now()
	weeks = calendar.Calendar(calendar.SUNDAY).monthdatescalendar(present.year, present.month)
	nweeks = []
	number_of_days = 0
	for week in weeks:
		nweek = []
		for day in week:
			if (number_of_days == 33):
				break
			if (day.month == present.month - 1 or day.month == present.month + 1):
				nweek.append({"day": None, "today": False, "month": present.month})
			elif (day.day == present.day and day.month == present.month):
				nweek.append({"day": day.day, "today": True, "month": present.month})
			else:
				nweek.append({"day": day.day, "today": False, "month": present.month})
			number_of_days += 1
		nweeks.append(nweek)
	return nweeks

from .General import *

def parseGradingSystem (field, value, row, index):
    if field == "ACTIVE":
        row[index] = bool(value)
    elif field == "LOWER_LIMIT" or field == "UPPER_LIMIT":
        row[index] = int(value)
    return row

def unparseGradingSystem (field, value, row, index):
    if field == "ACTIVE" or field == "LOWER_LIMIT" or field == "UPPER_LIMIT":
        row[index] = str(value)
    return row

def parseSchoolCalendar (field, value, row, index):
    if field == "DAY":
        row[index] = int(value)
    elif field == "BROADCAST":
        row[index] = bool(value)
    return row

def unparseSchoolCalendar (field, value, row, index):
    if field == "DAY":
        row[index] = str(value)
    elif field == "BROADCAST":
        row[index] = str(value)
    return row

def parseSchoolDepartments (field, value, row, index):
    if field == "ACTIVE":
        row[index] = bool(value)
    return row

def unparseSchoolDepartments (field, value, row, index):
    if field == "ACTIVE":
        row[index] = str(value)
    return row

def parseSchoolDivisions (field, value, row, index):
    if field == "ACTIVE":
        row[index] = bool(value)
    elif field == "SCHOOL_DIVISIONS":
        row[index] = jsonize(swapQuotes(value))
    return row

def unparseSchoolDivisions (field, value, row, index):
    if field == "ACTIVE":
        row[index] = str(value)
    elif field == "SCHOOL_DIVISIONS":
        row[index] = unjsonize(value)
    return row

def parseSchoolSubjects (field, value, row, index):
    if field == "TEACHERS" or field == "STUDENTS":
        row[index] = jsonize(swapQuotes(value))
        return row

def unparseSchoolSubjects (field, value, row, index):
    if field == "TEACHERS" or field == "STUDENTS":
        row[index] = unjsonize(value)
        return row

def parseResults (field, value, row, index):
    if field == "SCORE" or field == "OVERALL" or field == "PERCENTAGE":
        row[index] = int(value)
    return row

def unparseResults (field, value, row, index):
    if field == "SCORE" or field == "OVERALL" or field == "PERCENTAGE":
        row[index] = str(value)
    return row

def parseRunningProcesses (field, value, row, index):
    if field == "PID":
        row[index] = int(value)
    return row

def unparseRunningProcesses (field, value, row, index):
    if field == "PID":
        row[index] = str(value)
    return row

def parseWeeklyFields (field, value, row, index):
    if field == "FIELDS" or field == "MARKS":
        row[index] = jsonize(swapQuotes(value))
    elif field == "OVERALL":
        row[index] = int(value)
    return row

def unparseWeeklyFields (field, value, row, index):
    if field == "FIELDS" or field == "MARKS":
        row[index] = unjsonize(value)
    elif field == "OVERALL":
        row[index] = str(value)
    return row

def parseParents (field, value, row, index):
    if field == "WARDS":
        row[index] = jsonize(swapQuotes(value))
    return row

def unparseParents (field, value, row, index):
    if field == "WARDS":
        row[index] = unjsonize(value)
    return row

def parseStudents (field, value, row, index):
    if field == "AGE":
        row[index] = int(value)
    return row

def unparseStudents (field, value, row, index):
    if field == "AGE":
        row[index] = str(value)
    return row

def parseChatrooms (field, value, row, index):
    if (field == "FLOAT_TIME"):
        row[index] = float(value)
    return row

def unparseChatrooms (field, value, row, index):
    if (field == "FLOAT_TIME"):
        row[index] = str(value)
    return row

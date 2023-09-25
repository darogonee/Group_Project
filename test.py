import datetime
# print("2013-10-20T19:20:30+01:00")

# print(datetime.datetime.fromisocalendar(2014, 10, 6).isoformat())
# print(datetime.datetime.fromordinal(2014-10-6).isoformat())


# print(datetime.datetime.fromordinal(int("2014-10-6")).isoformat())

print((datetime.datetime(2021, 5, 1, 14, 0, 13)).isoformat())

value = "2021-5-1".split("-")
# print(value)
print((datetime.datetime(int(value[0]), int(value[1]), int(value[2]), 14, 0, 13)).isoformat())
datetime.datetime(int(value[0]), int(value[1]), int(value[2]), 14, 0, 13).isoformat()
# 1) Subtract five days from current date
from datetime import datetime, timedelta

now = datetime.now()
five_days_ago = now - timedelta(days=5)
print(five_days_ago)


# 2) Print yesterday, today, tomorrow
from datetime import date, timedelta

today = date.today()
yesterday = today - timedelta(days=1)
tomorrow = today + timedelta(days=1)

print("Yesterday:", yesterday)
print("Today:", today)
print("Tomorrow:", tomorrow)

# 3) Drop microseconds from datetime
from datetime import datetime

now = datetime.now()
no_microseconds = now.replace(microsecond=0)
print(no_microseconds)


# 4) Calculate two date difference in seconds
from datetime import datetime

d1_str = input("Enter first datetime (YYYY-MM-DD HH:MM:SS): ")
d2_str = input("Enter second datetime (YYYY-MM-DD HH:MM:SS): ")

d1 = datetime.strptime(d1_str, "%Y-%m-%d %H:%M:%S")
d2 = datetime.strptime(d2_str, "%Y-%m-%d %H:%M:%S")

diff_seconds = abs((d2 - d1).total_seconds())
print(int(diff_seconds))
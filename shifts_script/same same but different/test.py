from datetime import date, datetime, timedelta

now = datetime.utcnow().isoformat() + 'Z'
print(now)
now_str = str(now)
current_day_date = date.today() #datetime.utcnow().isoformat() + 'Z' # date.today()
this_sunday_date = current_day_date - timedelta(days = (current_day_date.weekday() + 1) % 7)
sunday_time = '08:00:00.000000Z'
s = f'{this_sunday_date}T{sunday_time}'
# isostring = datetime.strptime(f'{this_sunday_date} {sunday_time}', '%Y-%m-%d %H:%M:%S.{0}').isoformat()
print(s)
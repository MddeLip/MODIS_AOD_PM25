import datetime

print(datetime.datetime.now())
print(datetime.datetime.now()+datetime.timedelta(hours=-24))


def get_new_time(x):
    x = x+datetime.timedelta(hours=1)
    return x
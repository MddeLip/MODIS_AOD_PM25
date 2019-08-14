# -*- coding: utf-8 -*-
# 时间    : 2019/1/27 8:27
# 作者    : xcl

'''
输出格式:2018,1,1
'''
import datetime
import time
weekday = time.strptime('2017365', '%Y%j')
weekday = time.strftime("%Y,%m,%d", weekday)

weekday = datetime.datetime.strptime(weekday, '%Y,%m,%d').date()
print(weekday,weekday.__class__)
#print(weekday.__class__)
delta = datetime.timedelta(days=1)
endtime = weekday + datetime.timedelta(days=365)
endtime = str(endtime.strftime('%Y,%m,%d'))
#print(weekday+delta,weekday,delta,sep="\n")
years = []
i = 0
#print(time.localtime())
for j in range(365):
    weekday += delta

    years.append(weekday)

#print(years.__class__)
years2 = []
for item in years:
    #print(item)
    item=(str(item)).replace("-",",")
    years2.append(item)
#print(years2[1],years2[1][1])#,"\n",years2)
print(years2)

'''
while str(weekday.strftime('%Y,%m,%d ')) != "2018-12-31":
     weekday += delta
     a = str(weekday.strftime('%Y,%m,%d'))
     years.append(a)

print(years)'''

import calendar
from datetime import datetime
now=datetime.now()
ye=now.date()
yea=list(str(ye))
year=int(yea[0]+yea[1]+yea[2]+yea[3])
age=input('Please enter your current age: ')
yr=int(year)-int(age)
mt=input('Enter the month you were born in: ')
dy=input('Enter the date of the month you were born in: ')
cal=calendar.weekday(int(yr),int(mt),int(dy))
day=['Mon','Tue','Wed','Thur','Fri','Sat','Sun']
month=['jan','feb','mar','april','may','jun','jul','aug','sept','oct','nov','dec']
print('\\\this is the day you were born on ',day[cal],dy, month[int(mt)-1], yr)



import datetime
print('THE PROGRAM TO OUT THE DATE OF BIRTH')
name=input('Whats your name : ')
y=int(input('Input the year of birth: '))
m= int(input('Input the month of birth: '))
d= int(input('Input the date of birth: '))


p = datetime.date(y,m,d)
print ( name, 'was born on', p.strftime('%a'))
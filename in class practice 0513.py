"""
in class practice 0513
"""

#build a class Time
class Time():
#static variable - for all objects of Time, later affects print fcns
  hour_in_12 = False #default is 24 hr mode

#constructor - makes the instance variables as the obj is created
  def __init__(self, h, m, s):#int
    self.hour = h
    self.minute = m
    self.second = s

  def print_normally(self):
    print("%d:%d:%d" % (self.hour, self.minute, self.second),end = "")

  def print_two_digits(self,n):#判斷是否為兩位數
  
    if(n < 10):
      print(0, end = "")
    
    print(n, end = "")
  
  def print_nicely(self):
    
    if (Time.hour_in_12 == False) or (self.hour < 12):
      self.print_two_digits(self.hour)
    else:
      self.print_two_digits(self.hour - 12)
    print(":",end = "")
    self.print_two_digits(self.minute)
    print(":",end = "")
    self.print_two_digits(self.second)
	
    if Time.hour_in_12 == True:
      print("PM")	

  def is_earlier_than(self, t):
    selftime = self.hour * 3600 + self.minute * 60 +self.second
    anothertime = t.hour * 3600 + t.minute *60 + t.second
    if selftime < anothertime:
      return True
    elif selftime >= anothertime:
      return False
	  
"""	  
#Problem 1  
t1 = Time(9, 8, 4)
t2 = Time(13, 10, 5)
if t1.is_earlier_than(t2):
  t1.print_nicely()
else:
  t2.print_nicely()

"""
#Problem 2 
inList = input().split()
inList = [int(i) for i in inList]
print(inList)
#create object with the input data
t1 = Time(inList[0],inList[1], inList[2])
t2 = Time(inList[3],inList[4], inList[5])
t3 = Time(inList[6],inList[7], inList[8])

#what mode is it?
mode = input("Enter 12 or 24 as mode:  ")
if mode == "12":
  Time.hour_in_12 = True
elif mode == "24":
  Time.hour_in_12 = False
  
  
#use the inst fcn is_earlier_than to find the earliest of the three
if t1.is_earlier_than(t2):
  if t1.is_earlier_than(t3):
    t1.print_nicely()
  elif t3.is_earlier_than(t1):
    t3.print_nicely()
else: 
  if t2.is_earlier_than(t3):
    t2.print_nicely()
  elif t3.is_earlier_than(t2):
    t3.print_nicely()



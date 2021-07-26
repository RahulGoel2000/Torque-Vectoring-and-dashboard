import csv

myData = ['32','33','34','35']
myFile = open('123.csv', 'a+')
with myFile:
   writer = csv.writer(myFile)
   writer.writerows(myData)
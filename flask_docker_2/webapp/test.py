import re
text = open("/home/foxy/VScode/flask_docker/webapp/test.txt", "r")
#text = ' "location": {"country": "United States of America",'
country = re.search(r'"country": "[a-zA-Z -]*",',text.read())
#country = re.search(r'"country": "[a-zA-Z -]*",',text)
print(country.group(0))
from datetime import date

today = date.today()
print("Today's date:", today)
dt = '2023-03-03'
dt = dt.split('-')
dt[1] = re.sub(r'0\d', 
             dt[1][1], dt[1])
dt[2] = re.sub(r'0\d', 
             dt[2][1], dt[1])
#dt[2].replace(r'\d{1}0',r'\d')
print(dt)
diff = date(int(dt[0]),int(dt[1]),int(dt[2])) - today
print(diff.days)
print(date(int(dt[0]),int(dt[1]),int(dt[2])))
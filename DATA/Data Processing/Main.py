
import fastf1
from Results import get_result

print("Tell me the race you want to know about")

date = input("Race year: ")
date_int = int(date)  # Convert string to integer
if(date_int > 1990 and date_int <= 2025):
    print("Date is good")
    date = str(date_int)
else:
    print("error")
    
race_name = input("Race name: ")
race_type = input("Select, FP1, FP2, Q, R: ")

print(get_result(date, race_name, race_type))


import fastf1
from race_result import get_race_result
from qualifying_result import get_qualifying_result
from sprint_result import get_sprint_result

Year = [2025 ,2024, 2023, 2022, 2021, 2020, 2019, 2018, 2017]
race_type = ["R", "Q", "S"]

for year in Year:
    schedule = fastf1.get_event_schedule(year)
    Name = [schedule["EventName"].unique()]
    
    for name in Name[0]:
        for race in race_type:
            if race == "R": 
                get_race_result(str(year), name, race)
            elif race == "Q":
                get_qualifying_result(str(year), name,race)
            elif race == "S":
                get_sprint_result(str(year), name, race)


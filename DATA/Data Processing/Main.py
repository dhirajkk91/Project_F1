
import fastf1
from result import get_result

fastf1.Cache.enable_cache('DATA/Data%20Processing/_pycache_')

Year = [2025 ,2024, 2023, 2022, 2021, 2020, 2019, 2018, 2017]

for year in Year:
    schedule = fastf1.get_event_schedule(year)
    Name = [schedule["EventName"].unique()]
    
    for name in Name[0]:
        print(f"Getting results for {name} {year}...")
        get_result(str(year), name, "R")


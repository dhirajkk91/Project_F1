
import fastf1
from race_result import get_race_result
from qualifying_result import get_qualifying_result
from sprint_result import get_sprint_result

Year = [2025, 2024, 2023, 2022, 2021, 2020, 2019, 2018]
race_type = ["R", "Q", "S"]

for year in Year:
    try:
        schedule = fastf1.get_event_schedule(year)
    except Exception as e:
        print(f"Warning: could not load schedule for {year}: {e}")
        print("Skipping this year.")
        continue

    event_names = schedule.get("EventName")
    if event_names is None:
        print(f"Warning: no EventName column in schedule for {year}, skipping year.")
        continue

    for name in event_names.unique():
        # Quick probe: check if fastf1 has any session for this event. If none, skip to next event.
        possible_session_types = ["R", "Q", "S"]
        found_session = False
        for st in possible_session_types:
            try:
                fastf1.get_session(year, name, st)
                found_session = True
                break
            except Exception:
                # session type not available for this event; try next
                continue

        if not found_session:
            print(f"No sessions found for event '{name}' in {year} (fastf1 has no data) - skipping event.")
            continue

        for race in race_type:
            try:
                if race == "R":
                    get_race_result(str(year), name, race)
                elif race == "Q":
                    get_qualifying_result(str(year), name, race)
                elif race == "S":
                    get_sprint_result(str(year), name, race)
            except ValueError as e:
                # Specific fastf1 ValueErrors (session not found, conversion issues) - skip
                print(f"ValueError for {name} {year} ({race}): {e} - skipping this session.")
                continue
            except Exception as e:
                # Generic catch - log and continue
                print(f"Error processing {name} {year} ({race}): {e} - continuing to next.")
                continue


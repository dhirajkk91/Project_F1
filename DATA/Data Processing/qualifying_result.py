import fastf1
import pandas as pd
import os

def get_qualifying_result(date, race_name, race_type):
    
    # Convert date to integer for fastf1
    year = int(date)
        
        # Get the session using actual variable values (not string literals)
    session = fastf1.get_session(year, race_name, race_type)
        
        # Load the session data
    session.load()
        
        # Get the results data
    results = session.results
        
        # Convert to DataFrame
    df = pd.DataFrame(results)
    
    if (race_type == "Q"):
        try:

        # Removing the unnecessary columns
            df = df.drop(columns = ["DriverId", "BroadcastName","HeadshotUrl", "CountryCode", "TeamColor", "Time", "Points","Laps","GridPosition","TeamId", "Status" , "ClassifiedPosition"  ], axis=1)

        # Fixing the timing structure of the qualifying drivers
            qualifying_columns = ['Q1', 'Q2', 'Q3']
            
            for col in qualifying_columns:
                if col in df.columns:
                    formatted_times = []
                    for time in df[col]:
                        if pd.isna(time):
                            formatted_times.append("N/A")
                        else:
                            # Convert timedelta to proper string format
                            total_seconds = time.total_seconds()
                            minutes = int(total_seconds // 60)
                            seconds = total_seconds % 60
                            # Format as "M:SS.sss"
                            formatted_time = f"{minutes}:{seconds:06.3f}"
                            formatted_times.append(formatted_time)
                    df[col] = formatted_times
        
        # Create the database folder if it doesn't exist
            database_folder = fr"C:\Users\dhira\OneDrive\Desktop\Projects\Project_F1\DATA\DataBase\Results\{year}\Qualifying"
            os.makedirs(database_folder, exist_ok=True)
        
        # Create filename with race details and timestamp to avoid conflicts
            filename = f"{year}_{race_name.replace(' ', '_')}_{race_type}.csv"
            filepath = os.path.join(database_folder, filename)
        
        # Save DataFrame to CSV
            df.to_csv(filepath, index=False)
        
            return f"Successfully saved {race_type} results for {race_name} {year} to {filepath}"
        
        except Exception as e:
            return f"Error loading session: {str(e)}"

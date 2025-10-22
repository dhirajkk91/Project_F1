import fastf1
import pandas as pd
import os

def get_result(date, race_name, race_type):
    """Get F1 session data using fastf1 library and save to CSV"""
    
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
            
    if (race_type == "R"):
        try:
        # Removing the unnecessary columns
            df = df.drop(columns = ["HeadshotUrl","Q1", "Q2","Q3","Points","DriverId", "CountryCode", "TeamColor", "TeamId", "BroadcastName", "FirstName", "LastName"], axis = 1)

        # Fixing the timing structure of the race drivers
            if 'Time' in df.columns and len(df) > 0:
                print("Processing time column...")  # Debug info
                
                # Create a new list to store formatted times
                formatted_times = []
                
                for i in range(len(df)):
                    current_time = df.iloc[i]['Time']
                    
                    if i == 0:
                        # First driver: convert to string format to prevent Excel auto-formatting
                        if pd.isna(current_time):
                            formatted_times.append("N/A")
                        else:
                            # Convert timedelta to proper string format
                            total_seconds = current_time.total_seconds()
                            hours = int(total_seconds // 3600)
                            minutes = int((total_seconds % 3600) // 60)
                            seconds = total_seconds % 60
                            # Format as "H:MM:SS.sss" string with apostrophe to force text format
                            time_str = f"'{hours}:{minutes:02d}:{seconds:06.3f}"
                            formatted_times.append(time_str)
                    else:
                        # Other drivers: the Time column already contains the gap from winner
                        if pd.isna(current_time):
                            formatted_times.append("N/A")
                        else:
                            # Convert the time gap to +X.XXX sec format
                            gap_seconds = current_time.total_seconds()
                            formatted_times.append(f"+{gap_seconds:.3f} sec")
                
                # Replace the entire Time column with formatted values
                df['Time'] = formatted_times
                print("Time formatting completed!")  # Debug info
            
        
        # Create the database folder if it doesn't exist
            database_folder = fr"C:\Users\dhira\OneDrive\Desktop\Projects\Project_F1\DATA\DataBase\Results\{year}\Race"
            os.makedirs(database_folder, exist_ok=True)
        
        # Create filename with race details and timestamp to avoid conflicts
            filename = f"{year}_{race_name.replace(' ', '_')}_{race_type}.csv"
            filepath = os.path.join(database_folder, filename)
        
        # Save DataFrame to CSV
            df.to_csv(filepath, index=False)
        
            return f"Successfully saved {race_type} results for {race_name} {year} to {filepath}"
        
        except Exception as e:
            return f"Error loading session: {str(e)}"
        
    elif (race_type == "Q"):
        
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

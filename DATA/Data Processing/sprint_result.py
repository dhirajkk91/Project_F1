import fastf1
import pandas as pd
import os

def get_sprint_result(date, race_name, race_type):
    """Get F1 sprint session data using fastf1 library and save to CSV"""
    
    # Convert date to integer for fastf1
    year = int(date)
        
    try:
        
        try:
            session = fastf1.get_session(year, race_name, "S")
        except:
            return f"No sprint session available for {race_name} {year}"
        
        # Load the session data
        session.load()
        
        # Get the results data
        results = session.results
        
        # Convert to DataFrame
        df = pd.DataFrame(results)
    
        # Main processing block
        df = df.drop(columns = ["HeadshotUrl","Q1", "Q2","Q3","Points","DriverId", "CountryCode", "TeamColor", "TeamId", "BroadcastName", "FirstName", "LastName"], axis = 1)
        
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
                        time_str = f"{hours}:{minutes:02d}:{seconds:06.3f}"
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
            database_folder = fr"C:\Users\dhira\OneDrive\Desktop\Projects\Project_F1\DATA\DataBase\Results\{year}\Sprint"
            os.makedirs(database_folder, exist_ok=True)
        
            # Create filename with race details and timestamp to avoid conflicts
            filename = f"{year}_{race_name.replace(' ', '_')}_{race_type}.csv"
            filepath = os.path.join(database_folder, filename)
        
            # Save DataFrame to CSV
            df.to_csv(filepath, index=False)
        
            return f"Successfully saved {race_type} results for {race_name} {year} to {filepath}"

    except Exception as e:
        # Any unexpected error during session retrieval or processing
        return f"Error processing sprint session for {race_name} {year}: {str(e)}"


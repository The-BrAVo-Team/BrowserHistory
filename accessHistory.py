import sqlite3
from epochConverter import epochConverter
import dateTime

def fetch_history(db_path="C:\\Users\\keoca\\Desktop\\TWP3\\TestUser\\Default\\History"):
    """
    Fetches browsing history from the SQLite database.
    """
    try:
        con = sqlite3.connect(db_path)
        cur = con.cursor()
        res = cur.execute("SELECT url FROM urls ORDER BY last_visit_time")
        history = res.fetchall()
        con.close()
        return [url[0] for url in history]  # Return a list of URLs
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return []
    
    
def modify_timestamps(start_date, end_date, start_time, end_time, db_path="C:\\Users\\keoca\\Desktop\\TWP3\\TestUser\\Default\\History"):
    dateTimeList = dateTime.create_date_time_output(start_date, end_date, start_time, end_time)
    
    try:
        con = sqlite3.connect(db_path)
        cur = con.cursor()
        
        for date_time in dateTimeList:
            webkit_timestamp = epochConverter.date_to_webkit(date_time)
            
            # Update the timestamp for all URLs (or add filtering logic if needed)
            cur.execute("UPDATE urls SET last_visit_time = ? WHERE last_visit_time IS NOT NULL", (webkit_timestamp,))
            
        
        con.commit()
        con.close()
        print("Timestamps updated successfully.")
    
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    modify_timestamps("2024-04-14", "2024-05-14", "20:00:00", "23:59:59")
    history = fetch_history()
    for url in history:
        print(url)

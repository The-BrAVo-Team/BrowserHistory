import sqlite3

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

if __name__ == '__main__':
    history = fetch_history()
    for url in history:
        print(url)

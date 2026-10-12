import mysql.connector

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "Atharv",
    "database": "eventhopia"
}

def remove_duplicates():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    
    # Identify the IDs to keep (the minimum ID for each email/event pair)
    keep_query = """
        SELECT MIN(id) as id
        FROM registrations_new
        GROUP BY email, event_id
    """
    cursor.execute(keep_query)
    keep_ids = [row['id'] for row in cursor.fetchall()]
    
    if not keep_ids:
        print("No registrations found.")
        return

    # Delete everything NOT in the keep list
    # Using a list in the query
    format_strings = ','.join(['%s'] * len(keep_ids))
    delete_query = f"DELETE FROM registrations_new WHERE id NOT IN ({format_strings})"
    
    cursor.execute("SELECT COUNT(*) as cnt FROM registrations_new")
    total_before = cursor.fetchone()['cnt']
    
    cursor.execute(delete_query, keep_ids)
    conn.commit()
    
    cursor.execute("SELECT COUNT(*) as cnt FROM registrations_new")
    total_after = cursor.fetchone()['cnt']
    
    print(f"Cleanup complete!")
    print(f"Total entries before: {total_before}")
    print(f"Total entries after:  {total_after}")
    print(f"Removed {total_before - total_after} duplicate entries.")
    
    cursor.close()
    conn.close()

if __name__ == "__main__":
    remove_duplicates()

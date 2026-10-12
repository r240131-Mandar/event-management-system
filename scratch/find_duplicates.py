import mysql.connector

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "Atharv",
    "database": "eventhopia"
}

def find_duplicates():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    
    # Find emails that appear more than once for the same event
    query = """
        SELECT email, event_id, COUNT(*) as count
        FROM registrations_new
        GROUP BY email, event_id
        HAVING COUNT(*) > 1
    """
    cursor.execute(query)
    duplicates = cursor.fetchall()
    
    if not duplicates:
        print("No duplicate registrations found.")
        return
    
    print(f"Found {len(duplicates)} sets of duplicates:\n")
    for dup in duplicates:
        print(f"Email: {dup['email']} | Event ID: {dup['event_id']} | Count: {dup['count']}")
        
        # List the individual entries
        cursor.execute("SELECT id, name, ticket_id, status FROM registrations_new WHERE email=%s AND event_id=%s", (dup['email'], dup['event_id']))
        entries = cursor.fetchall()
        for e in entries:
            print(f"  - ID: {e['id']} | Name: {e['name']} | Ticket: {e['ticket_id']} | Status: {e['status']}")
    
    cursor.close()
    conn.close()

if __name__ == "__main__":
    find_duplicates()

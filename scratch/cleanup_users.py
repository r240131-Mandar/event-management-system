import mysql.connector

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "Atharv",
    "database": "eventhopia"
}

def cleanup_users():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    
    # 1. Find duplicate emails in 'users' table
    cursor.execute("""
        SELECT email, COUNT(*) as count
        FROM users
        WHERE email IS NOT NULL AND email != ''
        GROUP BY email
        HAVING COUNT(*) > 1
    """)
    duplicates = cursor.fetchall()
    
    if not duplicates:
        print("No duplicate user emails found.")
    else:
        print(f"Found {len(duplicates)} sets of duplicate user emails.")
        for dup in duplicates:
            print(f"Email: {dup['email']} | Count: {dup['count']}")
            # Keep the first user (lowest ID)
            cursor.execute("SELECT id, username FROM users WHERE email=%s ORDER BY id ASC", (dup['email'],))
            users = cursor.fetchall()
            keep_id = users[0]['id']
            delete_ids = [u['id'] for u in users[1:]]
            
            print(f"  Keeping: {users[0]['username']} (ID: {keep_id})")
            for u in users[1:]:
                print(f"  Deleting: {u['username']} (ID: {u['id']})")
            
            # Delete duplicates
            if delete_ids:
                format_strings = ','.join(['%s'] * len(delete_ids))
                cursor.execute(f"DELETE FROM users WHERE id IN ({format_strings})", delete_ids)
        
        conn.commit()
        print("User cleanup complete.\n")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    cleanup_users()

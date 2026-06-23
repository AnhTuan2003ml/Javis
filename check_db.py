import sqlite3

try:
    con = sqlite3.connect("jarvis.db")
    cursor = con.cursor()
    
    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("Tables in database:")
    for table in tables:
        print(f"- {table[0]}")
    
    # Check web_command table if it exists
    try:
        cursor.execute("SELECT * FROM web_command")
        web_commands = cursor.fetchall()
        print("\nWeb commands:")
        for cmd in web_commands:
            print(f"- {cmd}")
            if "goodreads" in str(cmd).lower():
                print(f"  *** FOUND GOODREADS: {cmd}")
    except:
        print("No web_command table found")
    
    # Check sys_command table if it exists
    try:
        cursor.execute("SELECT * FROM sys_command")
        sys_commands = cursor.fetchall()
        print("\nSystem commands:")
        for cmd in sys_commands:
            print(f"- {cmd}")
            if "goodreads" in str(cmd).lower():
                print(f"  *** FOUND GOODREADS: {cmd}")
    except:
        print("No sys_command table found")
    
    con.close()
    
except Exception as e:
    print(f"Error: {e}")
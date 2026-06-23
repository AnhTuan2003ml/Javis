import sqlite3

con = sqlite3.connect("jarvis.db")
cursor = con.cursor()

# Show contacts with IDs first
cursor.execute("SELECT rowid, name, mobile_no FROM contacts")
results = cursor.fetchall()

print("Current contacts:")
for contact in results:
    print(f"ID: {contact[0]}, Name: {contact[1]}, Number: {contact[2]}")

# Delete contact with ID 4
cursor.execute("DELETE FROM contacts WHERE rowid = 4")
con.commit()

print(f"\nDeleted contact with ID 4")

# Show remaining contacts
cursor.execute("SELECT rowid, name, mobile_no FROM contacts")
results = cursor.fetchall()

print("\nRemaining contacts:")
for contact in results:
    print(f"ID: {contact[0]}, Name: {contact[1]}, Number: {contact[2]}")

con.close()
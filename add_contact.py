import sqlite3

def add_contact(name, mobile_no):
    """Add contact to jarvis.db"""
    con = sqlite3.connect("jarvis.db")
    cursor = con.cursor()
    
    try:
        cursor.execute("INSERT INTO contacts (name, mobile_no) VALUES (?, ?)", (name, mobile_no))
        con.commit()
        print(f"Contact added: {name} - {mobile_no}")
    except Exception as e:
        print(f"Error adding contact: {e}")
    finally:
        con.close()

def view_contacts():
    """View all contacts"""
    con = sqlite3.connect("jarvis.db")
    cursor = con.cursor()
    
    try:
        cursor.execute("SELECT name, mobile_no FROM contacts")
        contacts = cursor.fetchall()
        
        if contacts:
            print("Contacts:")
            for name, mobile in contacts:
                print(f"{name}: {mobile}")
        else:
            print("No contacts found")
    except Exception as e:
        print(f"Error viewing contacts: {e}")
    finally:
        con.close()

if __name__ == "__main__":
    print("1. Add Contact")
    print("2. View Contacts")
    choice = input("Choose option: ")
    
    if choice == "1":
        name = input("Enter name: ")
        mobile = input("Enter mobile number: ")
        add_contact(name, mobile)
    elif choice == "2":
        view_contacts()
import sqlite3

con = sqlite3.connect("jarvis.db")
cursor = con.cursor()

# Create tables
cursor.execute("CREATE TABLE IF NOT EXISTS sys_command(id integer primary key, name VARCHAR(100), path VARCHAR(1000))")
cursor.execute("CREATE TABLE IF NOT EXISTS web_command(id integer primary key, name VARCHAR(100), url VARCHAR(1000))")

# Add common PC applications
pc_apps = [
    ("notepad", "notepad.exe"),
    ("calculator", "calc.exe"),
    ("paint", "mspaint.exe"),
    ("chrome", "chrome.exe"),
    ("firefox", "firefox.exe"),
    ("edge", "msedge.exe"),
    ("word", "winword.exe"),
    ("excel", "excel.exe"),
    ("powerpoint", "powerpnt.exe"),
    ("cmd", "cmd.exe"),
    ("task manager", "taskmgr.exe"),
]

# Add common websites
websites = [
    ("youtube", "https://www.youtube.com"),
    ("google", "https://www.google.com"),
    ("facebook", "https://www.facebook.com"),
    ("instagram", "https://www.instagram.com"),
    ("twitter", "https://www.twitter.com"),
    ("gmail", "https://mail.google.com"),
    ("netflix", "https://www.netflix.com"),
    ("amazon", "https://www.amazon.com"),
]

print("Adding PC applications...")
for name, path in pc_apps:
    cursor.execute("INSERT OR REPLACE INTO sys_command VALUES (null, ?, ?)", (name, path))
    print(f"Added: {name}")

print("\nAdding websites...")
for name, url in websites:
    cursor.execute("INSERT OR REPLACE INTO web_command VALUES (null, ?, ?)", (name, url))
    print(f"Added: {name}")

con.commit()
con.close()

print(f"\n✓ Added {len(pc_apps)} PC apps and {len(websites)} websites!")
print("\nNow you can say:")
print("  'open notepad' - Opens PC notepad")
print("  'open whatsapp' - Opens WhatsApp on phone")
print("  'open youtube' - Opens YouTube website")
print("  'open instagram' - Opens Instagram on phone")
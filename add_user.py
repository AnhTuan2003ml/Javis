#!/usr/bin/env python3
import json

def add_user():
    try:
        with open('users.json', 'r') as f:
            users = json.load(f)
    except FileNotFoundError:
        users = {}
    
    user_id = input("Enter user ID: ")
    name = input("Enter user name: ")
    
    users[user_id] = name
    
    with open('users.json', 'w') as f:
        json.dump(users, f, indent=2)
    
    print(f"User {name} (ID: {user_id}) added successfully!")
    print("Current users:")
    for uid, uname in users.items():
        print(f"  ID: {uid}, Name: {uname}")

if __name__ == "__main__":
    add_user()
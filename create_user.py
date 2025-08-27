import json

    

def gamble(username):
    with open("users.json", "r") as file:
        json_users = json.load(file)
    for json_user in json_users:
        if username == json_user["name"]:
            correct_user = json_user

def create_user():
    with open("users.json", "r") as file:
        json_users = json.load(file)
    json_usernames = []
    for json_user in json_users:
        print(json_user["name"])
        json_usernames.append(json_user["name"].lower())
    
    print("The above usernames are already taken. ")
    
    desired_username = input("Please select a username for your account. ")
    if desired_username.lower() in json_usernames:
        print("Invalid username.")
    else:
        new_user = {
            "name": desired_username,
            "current_streak" : 0,
            "horse_bucks" : 500 
        }
        json_users.append(new_user)
        with open("users.json", "w") as file:
            json_users = json.dump(json_users, file, indent=2)
            
create_user()
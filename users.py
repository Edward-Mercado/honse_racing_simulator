import json

def gamble(selected_horses):
    with open("users.json", "r") as file:
        json_users = json.load(file)
    
    for i in range(len(json_users)):
        print(f"{(i)}: {json_users[i]["name"]}")
    
    selected_users = []
    done = False
    while done == False:
        try:
            user = json_users[int(input("Select the ID of the user you want to gamble with or enter done to finish. "))]
            selected_users.append(user)
            if len(selected_users) == len(json_users):
                done = True
        except:
            done = True
    
    users_with_bets = []
    for user in selected_users:
        print("")
        print(f"USERNAME: {user['name']}")
        print(f"HONSE BUCKS: {user["honse_bucks"]}")
        print(f"CURRENT_STREAK: {user["current_streak"]}")
        print(f"LIFETIME CORRECT GUESSES: {user["lifetime_correct_guesses"]}")
        print("")
        try:
            honse_buck_bet = int(input("How many Honse Bucks would you like to use? "))
            if honse_buck_bet > user["honse_bucks"]:
                print("Going all in. ")
                honse_buck_bet = user["honse_bucks"]
            elif honse_buck_bet == 0:
                print("coward.")    
            
        except:
            print("Invalid Honse Buck bet amount. Bet is set to 0.")
            honse_buck_bet = 0
        
        user["honse_bucks"] -= honse_buck_bet
        
        print("")
        for i in range(len(selected_horses)):
            print(f"{i}: {selected_horses[i]}")
        print("")
        try:
            selected_horse = selected_horses[int(input("Select the ID of the horse you wish to bet on. "))]
            print(f"You have successfully placed a {honse_buck_bet} Honse Dollar Bet for {selected_horses[i]}!")
        except:
            selected_horse = selected_horses[0]
            print(f"Invalid input. Your {honse_buck_bet} Honse Dollar bet has automatically been placed as {selected_horse}.")
            
        users_with_bets.append([user, honse_buck_bet, selected_horse])
    return users_with_bets
            
def delete_user():
    with open("users.json", "r") as file:
        json_users = json.load(file)
        
    for i in range(len(json_users)):
        print(f"{i}: {json_users[i]["name"]}")
    
    try:
        delete_user_target = json_users[int(input("Select the number of the user you wish to delete."))]
        
        if delete_user_target["current_streak"] > 2 or delete_user_target["honse_bucks"] > 1000:
            if delete_user_target["current_streak"] > 2:
                message_1 = "It has a very high streak! "
            else:
                message_1 = ""
            
            if delete_user_target["honse_bucks"] > 1000:
                message_2 = "It has a lot of honse bucks!"
            else:
                message_2 = ""
            
            print(f"This is a valuable account! {message_1}{message_2}")
            if delete_user_target["current_streak"] > 2:
                print("")
            confirmation = input("Enter Y to confirm: ")
        else:
            confirmation = "Y"
        
        if confirmation.upper() == "Y":
            json_users.remove(delete_user_target) 
            with open("users.json", "w") as file:
                json.dump(json_users, file, indent=4)
                print("Account successfully deleted!")
        else:
            print("Account deletion cancelled.")
    except:
        print("Invalid input. Account deletion cancelled.")
    
def create_user():
    with open("users.json", "r") as file:
        json_users = json.load(file)
        
    json_usernames = []
    for json_user in json_users:
        print(json_user["name"])
        json_usernames.append(json_user["name"].lower())
    
    print("The above usernames are already taken. ")
    
    
    desired_username = input("Please select a username for your account. ")
    if desired_username.lower() in json_usernames and desired_username.lower() != "done":
        print("Invalid username.")
    else:
        new_user = {
            "name": desired_username,
            "current_streak" : 0,
            "honse_bucks" : 500,
            "lifetime_correct_guesses": 0
        }
        json_users.append(new_user)
        with open("users.json", "w") as file:
            json_users = json.dump(json_users, file, indent=4)
            print("Account successfully created!")
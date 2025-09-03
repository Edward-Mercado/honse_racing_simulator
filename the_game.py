from screen import Screen
from users import gamble
import json, random

def play_the_game(random_on, map_chosen, participating_horses, gambling, max_fps, map_choice):
    # the list of horses
    all_horses = ["Aquamarine Gambit", "Barred Enchantment", "Cherry Jubilee", "Christ Almighty", "Crybaby Sundae", "Dabloon Matey", "Ellsee Reins", 
                "Finneas Cutlass", "Hopeless Endeavor", "Imperial Grace", "Jane Silksong", "John Horse", "Jovial Merryment", 
                "Lightning Strikes Thrice", "Maiden O'Luck", "Marshmallow Fluff", "Slow 'n' Steady", "The Sweetest Treat"]

    # the list of maps
    all_maps = ["Blank Field", "Bouncy Town", "The Wall-y West", "Mover Maze", 
                "The Stanky Leg", "Plinko Paradise", "Teleporting Mess", "Plinko Purgatory", "Knife Battlegrounds", 
                "Raceday The Thirteenth", "Honseday The Thirteenth", "Knifeday The Thirteenth"]

    # get the json files
    with open("horses.json", "r") as file:
        json_horses = json.load(file)
        
    with open("maps.json", "r") as file:
        json_maps = json.load(file)
        
    with open("users.json", "r") as file:
        json_users = json.load(file)
        
    for a_map in all_maps:
        map_index = all_maps.index(a_map)
        # map index will allow you to enter the map you want
        # and then it will show you which map you are opening
        print(f"{map_index}: {a_map}")

    # ask which map you want


    if map_chosen == False:
        map_choice = all_maps[random.randint(0, len(all_maps)-1)]

    for json_map in json_maps: # find the map chosen by the user
        if json_map["name"] == map_choice:
            chosen_map = json_map
            break

    # if its honseday then you cant pick hopeless endeavor as a race horse
    if chosen_map["name"] == "Honseday The Thirteenth":
        all_horses.remove("Hopeless Endeavor")
        print("This is a special gamemode.")

    if random_on == True:
        for horse in participating_horses:
            all_horses.remove(horse)
        
        while chosen_map["max_horses"] > len(participating_horses): # this will randomly pick the exact number of horses you need
            chosen_horse = random.choice(all_horses)
            participating_horses.append(chosen_horse)  
            all_horses.remove(chosen_horse)


    if gambling == True:
        if chosen_map["name"] == "Honseday The Thirteenth":
            participating_horses.append("Hopeless Endeavor")
        users_with_bets = gamble(participating_horses)
        if chosen_map["name"] == "Honseday The Thirteenth":
            participating_horses.remove("Hopeless Endeavor")
            
    if chosen_map["name"] != "Honseday The Thirteenth": # route the game to the correct mode
        winning_horse = Screen.game(participating_horses, map_choice, max_fps)
    else:
        winning_horse = Screen.honseday_the_thirteenth(participating_horses, map_choice, max_fps)
        
    for horse in json_horses:
        if horse["name"] == winning_horse.name:
            winning_horse = horse
            break

    
    winning_horse["documented_wins"] += 1
    
    if gambling == True:
        users_post_game = []

        for user_with_bet in users_with_bets:
            users_post_game.append(user_with_bet[0])
            if user_with_bet[2] == winning_horse["name"]:
                honse_buck_payout = user_with_bet[1] + round((user_with_bet[1] / winning_horse["speed"]))
                user_with_bet[0]["lifetime_correct_guesses"] += 1
                user_with_bet[0]["honse_bucks"] += honse_buck_payout
                user_with_bet[0]["current_streak"] += 1
                print(f"{user_with_bet[0]["name"]} placed a correct bet and has earned {honse_buck_payout} Honse Bucks!")
                print(f"Their streak is now {user_with_bet[0]["current_streak"]}!")
            else:
                if user_with_bet[0]["honse_bucks"] == 0:
                    random_money = random.randint(1, 20) * 10
                    
                    if random.randint(1, 100) == 100:
                        random_money = 1000000
                        print("JACKPOT!")
                        
                    print(f"{user_with_bet[0]["name"]} went bankrupt. They will be given a pity payment of {random_money} Honse Bucks.")
                    user_with_bet[0]["honse_bucks"] += random_money
                user_with_bet[0]["current_streak"] = 0
                print(f"{user_with_bet[0]["name"]} was not so lucky. Better luck next time!")
                print("Their streak is now 0.")
            print("")
            
        with open("users.json", "w") as file:
            json.dump(users_post_game, file, indent=4)
            
    with open("horses.json", "w") as file:
        json.dump(json_horses, file, indent=4)
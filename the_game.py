from screen import Screen
import json, random

random_on = True
map_chosen = True
map_choice = "Honseday The Thirteenth"

# the list of horses
all_horses = ["Aquamarine Gambit", "Cherry Jubilee", "Crybaby Sundae", "Ellsee Reins", "Finneas Cutlass", 
              "Hopeless Endeavor", "Imperial Grace", "John Horse", "Jovial Merryment", "Lightning Strikes Thrice", 
              "Maiden O'Luck", "Marshmallow Fluff", "Slow 'n' Steady", "The Sweetest Treat"]

participating_horses = []

# the list of maps
all_maps = ["Blank Field", "Bouncy Town", "The Wall-y West", "Mover Maze", 
            "The Stanky Leg", "Plinko Paradise", "Teleporting Mess", "Plinko Purgatory", "Knife Battlegrounds", 
            "Raceday The Thirteenth", "Honseday The Thirteenth"]

# get the json files
with open("horses.json", "r") as file:
    json_horses = json.load(file)
    
with open("maps.json", "r") as file:
    json_maps = json.load(file)
    
for a_map in all_maps:
    map_index = all_maps.index(a_map)
    # map index will allow you to enter the map you want
    # and then it will show you which map you are opening
    print(f"{map_index}: {a_map}")

# ask which map you want


if map_chosen == False:
    try:
        map_choice = all_maps[int(input("Select Map #: "))]
    except:
        map_choice = "Blank Field"

for json_map in json_maps: # find the map chosen by the user
    if json_map["name"] == map_choice:
        chosen_map = json_map
        break

# if its honseday then you cant pick hopeless endeavor as a race horse
if chosen_map["name"] == "Honseday The Thirteenth":
    all_horses.remove("Hopeless Endeavor")
    print("This is a special gamemode.")

print("")

if random_on == False: # you can make random_on true at the top if you want the game to pick horses for you (typically done in testing)
    for horse in all_horses: # same sort of logic as the map input
        horse_index = all_horses.index(horse)
        print(f"{horse_index}: {horse}")

    print("")
    print(f"Select up to {chosen_map["max_horses"]} horses. Enter an invalid ID to start prematurely.")    
    print("")

    for i in range(chosen_map["max_horses"]):
        input_horse = input("Select A Horse ID: ")
        try:
            horse_name = all_horses[int(input_horse)]
            participating_horses.append(horse_name)
        except: # invalid values break the loop and then start the game
            break
else:
    for i in range(chosen_map["max_horses"]): # this will randomly pick the exact number of horses you need
        chosen_horse = random.choice(all_horses)
        participating_horses.append(chosen_horse)  
        all_horses.remove(chosen_horse)
        
if chosen_map["name"] != "Honseday The Thirteenth": # route the game to the correct mode
    Screen.game(participating_horses, map_choice)
else:
    Screen.honseday_the_thirteenth(participating_horses, map_choice)
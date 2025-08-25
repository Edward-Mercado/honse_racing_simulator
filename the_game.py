from screen import Screen
import json, random

all_horses = ["Aquamarine Gambit", "Cherry Jubilee", "Crybaby Sundae", "Ellsee Reins", "Finneas Cutlass", 
              "Hopeless Endeavor", "Imperial Grace", "John Horse", "Jovial Merryment", "Lightning Strikes Thrice", 
              "Maiden O'Luck", "Marshmallow Fluff", "Slow 'n' Steady", "The Sweetest Treat"]

random_on = True

participating_horses = []

all_maps = ["Blank Field", "Bouncy Town", "The Wall-y West", "Mover Maze", 
            "The Stanky Leg", "Plinko Paradise", "Teleporting Mess", "Plinko Purgatory", "Knife Battlegrounds", 
            "Raceday The Thirteenth", "Honseday The Thirteenth"]

with open("horses.json", "r") as file:
    json_horses = json.load(file)
    
with open("maps.json", "r") as file:
    json_maps = json.load(file)
    
for a_map in all_maps:
    map_index = all_maps.index(a_map)
    print(f"{map_index}: {a_map}")

map_choice = all_maps[int(input("Select Map #: "))]

for json_map in json_maps:
    if json_map["name"] == map_choice:
        chosen_map = json_map
        break

if chosen_map["name"] == "Honseday The Thirteenth":
    all_horses.remove("Hopeless Endeavor")

print("")

if random_on == False:
    for horse in all_horses:
        horse_index = all_horses.index(horse)
        print(f"{horse_index}: {horse}")

    print("")
    print(f"Select up to {chosen_map["max_horses"]} horses.")    
    print("")

    for i in range(chosen_map["max_horses"]):
        input_horse = input("Select A Horse ID: ")
        try:
            horse_name = all_horses[int(input_horse)]
            participating_horses.append(horse_name)
        except:
            break
else:
    for i in range(chosen_map["max_horses"]):
        chosen_horse = random.choice(all_horses)
        participating_horses.append(chosen_horse)  
        all_horses.remove(chosen_horse)
        
if chosen_map["name"] != "Honseday The Thirteenth":
    Screen.game(participating_horses, map_choice)
else:
    Screen.honseday_the_thirteenth(participating_horses, map_choice)
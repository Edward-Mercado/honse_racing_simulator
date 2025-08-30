from the_game import play_the_game

# customize the game here ---------------------------------------------------------------------------------------------- #
random_on = True        # random horses
gambling = True          # gamble with users from users.json
max_fps = 120             # change game speed

map_chosen = True        # skip map selection 
map_choice = "Knife Battlegrounds"  # name of the map if map_chosen = True

participating_horses = ["Crybaby Sundae", "Hopeless Endeavor", "John Horse", "Dabloon Matey"] # put horses you already want to see here

# customize the game here ---------------------------------------------------------------------------------------------- #

play_the_game(random_on, map_chosen, participating_horses, gambling, max_fps, map_choice)

all_horses = [
    "Aquamarine Gambit", 
    "Barred Enchantment",
    "Cherry Jubilee", 
    "Christ Almighty", 
    "Crybaby Sundae", 
    "Dabloon Matey", 
    "Ellsee Reins", 
    "Finneas Cutlass", 
    "Hopeless Endeavor", 
    "Imperial Grace", 
    "Jane Silksong",
    "John Horse",
    "Jovial Merryment", 
    "Lightning Strikes Thrice", 
    "Maiden O'Luck", 
    "Marshmallow Fluff", 
    "Slow 'n' Steady", 
    "The Sweetest Treat"
    ]

all_maps = [
    "Blank Field", 
    "Bouncy Town", 
    "The Wall-y West", 
    "Mover Maze", 
    "The Stanky Leg", 
    "Plinko Paradise", 
    "Teleporting Mess", 
    "Plinko Purgatory", 
    "Knife Battlegrounds", 
    "Raceday The Thirteenth", 
    "Honseday The Thirteenth", 
    "Knifeday The Thirteenth"
            ]
from the_game import play_the_game

all_horses = [
    "Aquamarine Gambit", 
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

    # the list of maps
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

# customize the game here ---------------------------------------------------------------------------------------------- #
random_on = True        # random horses
gambling = False          # gamble with users from users.json
max_fps = 48             # change game speed

map_chosen = True        # skip map selection 
map_choice = "Knife Battlegrounds"  # name of the map if map_chosen = True

participating_horses = [] # put horses you already want to see here

# customize the game here ---------------------------------------------------------------------------------------------- #

play_the_game(random_on, map_chosen, participating_horses, gambling, max_fps)
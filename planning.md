# STANDARD KNIFE GAMEPLAY DANUUNAAANU:

item? horse can pickup item
once collision is made
sprite would change to hold the object
bounce as normal
collide with other horse
item would drop and the horse gets damaged
no collisions for one second
disappears?

have item as its own class

holding_knife = bool
knife = (x, y, 20, 20)
if horse.rect.colliderect(pygame.Rect(knife.hitbox)):
    holding_knife = True
    knife = (10000, 0, 20, 20)

(horse collision conditional):
    if horse.holding_knife == True:
        collision_point = (opp_horse: x, y)
        opp_horse.lives -= 1
        if opp_horse.lives == 0:
            kill_that_bitch()
            (remove it from horse_objects)
        
        horse_holding_knife = False
        knife x knife y = (collision_point)

        send the horses like 20 pixels away !!!


# HONSEDAY THE THIRTEENTH

rest of the honses loaded normally (with get_start_pos_function)

append hopeless
hopeless -> in horse_objects list but does not handle collision

each frame:
if horse.name != "Hopeless Endeavor":
    check for carrot

for loop horses:
    if collide:
        if opp_horse.name == "Hopeless Endeavor":
            horse.lives -= 1
            if horse.lives == 0:
                kill_that_bitch()
                (remove it from horse_objects)
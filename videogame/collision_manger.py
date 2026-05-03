import pygame

"Updates mouse clicks and scoreboard"
def handle_click(mouse_position, targets_group, scoreboard):
  

    hit_detected = False  #Keeping track for whether we hit something or not

    #Goes through each target in the group
    for target in targets_group:

        #Checks if mouse clicks target
        if target.contains_point(mouse_position):

            target.click()
            target.kill()

            scoreboard.record_hit()

            hit_detected = True

            break

    #If no target was hit, we count it as a miss
    if not hit_detected:
        scoreboard.record_miss() #Update to record a miss

    return hit_detected

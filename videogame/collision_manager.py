import pygame

def handle_click(mouse_position, targets_group, scoreboard):
    """
    Checks if mouse click hit any target
    - If a target is hit, we remove it and record a hit for scoreboard
    - If nothing is hit,  we record it as a miss for scoreboard
    """

    hit_detected = False  # Keeping track for whether we hit something or not

    # Going through each target in the group
    for target in targets_group:

        # Checks if the mouse click is inside this target
        if target.contains_point(mouse_position):

            # Updates the target and removes it
            target.click()      # Update the target as clicked
            target.kill()       # Remove target from game

            # Updates scoreboard with a recorded hit
            scoreboard.record_hit()

            hit_detected = True

            # Stops checking after 1st hit to prevent hitting multiple overlapping targets
            break

    # If no target was hit, we count it as a miss
    if not hit_detected:
        scoreboard.record_miss() # Update to record a miss

    return hit_detected
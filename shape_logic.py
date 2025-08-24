import pygame, math

def get_circle_hitboxes(center, radius):
    circle_hitboxes = []
    diameter = 2 * radius
    center_x = center[0]
    center_y = center[1]
    
    circle_hitboxes.append(pygame.Rect(center_x, center_y - radius, 1, diameter))
    
    for i in range(radius):
        if i != 0:
            rect_height = 0
            """
            derivation:
            circle formula = r^2 = x^2 + y^2 (** is the operand for exponentiation)
            where x is the horizontal distance from the center, and y is the vertical distance (pythagorean theorem)
            i is the integration amount, therefore that is our horizontal distance
            and we need to find the vertical distance
            quickly substitute
            move the rect_height to the left side and the radius to the right
            r          x     y
            radius^2 = i^2 + rect_height^2
            
            - rect_height^2 = i^2 - radius^2
            absolute value (i^2 - r^2) as negative numbers cannot be rooted
            then square root
            """
            
            rect_height = math.ceil(math.sqrt(abs(i**2 - radius**2)))
            
            circle_hitboxes.append(pygame.Rect(center_x - i, center_y - rect_height, 1, rect_height*2))
            circle_hitboxes.append(pygame.Rect(center_x + i, center_y - rect_height, 1, rect_height*2))
            
    return circle_hitboxes

def get_line_hitboxes(start_pos, end_pos, thickness): # start_pos_x MUST BE LESS THAN end_pos_x
    line_hitboxes = []
    
    top_value = math.floor(thickness / 2)
    
    start_pos_x = start_pos[0]
    start_pos_y = start_pos[1]
    end_pos_x = end_pos[0]
    end_pos_y = end_pos[1]
    
    delta_x = end_pos_x - start_pos_x
    delta_y = end_pos_y - start_pos_y
    
    slope = delta_y / delta_x
    
    for i in range(delta_x):
        new_pos_y = start_pos_y + (slope*i)
        if slope <= 1:
            line_hitboxes.append(pygame.Rect(start_pos_x + i, new_pos_y - (top_value - 1), math.ceil(slope), thickness))
        else:
            line_hitboxes.append(pygame.Rect((start_pos_x + i) - 9, (new_pos_y - (top_value - 1)) + 9, thickness, math.ceil(slope)))
    
    
    return line_hitboxes
from src.config.settings import GRID_SIZE

def check_collision(pos1, pos2, threshold=GRID_SIZE):
    """Check if two positions collide within the given threshold"""
    x1, y1 = pos1
    x2, y2 = pos2
    return abs(x1 - x2) < threshold and abs(y1 - y2) < threshold

def check_wall_collision(pos, width, height):
    """Check if position collides with walls"""
    x, y = pos
    return x < 0 or x >= width or y < 0 or y >= height

def check_self_collision(positions):
    """Check if snake collides with itself"""
    head = positions[0]
    return head in positions[1:]

def check_enemy_collision(snake_head, enemy_pos):
    """Check if snake collides with enemy"""
    return check_collision(snake_head, enemy_pos)

def check_food_collision(snake_head, food_pos):
    """Check if snake collides with food"""
    return snake_head == food_pos  # Exact match for food collection
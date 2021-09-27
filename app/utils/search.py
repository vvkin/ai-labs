from app.config.types import Point, Path

def restore_path(start: Point, goal: Point, memory: dict[Point, float]) -> Path:
    path = [goal]
    
    while goal in memory:
        parent = memory[goal]
        if parent == start: break
        goal = parent
        path.append(parent)
 
    # path.reverse()
    return path

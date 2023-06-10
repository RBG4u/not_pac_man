import heapq


def find_path(graph, start, goal):
    queue = []
    heapq.heappush(queue, (0, start))
    visited = {start: None}
    cost_visited = {start: 0}

    while queue != []:
        current_cost, current_coord = heapq.heappop(queue)

        if current_coord == goal:
            queue = []
            continue
        
        for next_coord in graph[current_coord]:
            neight_coord = (next_coord[0], next_coord[1])
            new_cost = cost_visited[current_coord]
            
            if neight_coord not in cost_visited:
                priority_cost = new_cost + manhattan_distance(neight_coord, goal)
                heapq.heappush(queue, (priority_cost, neight_coord))
                cost_visited[neight_coord] = priority_cost
                visited[neight_coord] = current_coord
    
    path = []
    current = goal
    while current != start:
            path.append(current)
            current = visited[current]
    path.append(start)
    path.reverse()

    return path


def manhattan_distance(a, b):
    distance = abs(a[0] - b[0]) + abs(a[1] - b[1])
    return distance


def do_graph(field):
    graph = {}
    for i in range(len(field)):
        for j in range(len(field[i])):
            if field[i][j] == 0:
                graph[i, j] = []

    for i in range(len(field)):
        for j in range(len(field[i])):
            if field[i][j] == 0:
                if i > 0 and field[i-1][j] == 0:
                    graph[i, j].append([i-1, j])
                if i < len(field)-1 and field[i+1][j] == 0:
                    graph[i, j].append([i+1, j])
                if j > 0 and field[i][j-1] == 0:
                    graph[i, j].append([i, j-1])
                if j < len(field[i])-1 and field[i][j+1] == 0:
                    graph[i, j].append([i, j+1])

    return graph
  

def do_field(walls_coords):
    CELL = 40
    FIELD_SIZE = 27
    field = []

    for i in range(FIELD_SIZE):
        line = []
        for j in range(FIELD_SIZE):
            if i == 0 or j == 0 or i == 26 or j == 26:
                line.append(1)
            else:
                line.append(0)
        field.append(line)

    for coord in walls_coords:
        field[coord[0] // CELL][coord[1] // CELL] = 1

    return field

def ai_move(walls, player, enemy):
    CELL = 40
    enemy_coord = (enemy.rect.topleft[0] // CELL, enemy.rect.topleft[1] // CELL)
    player_coord = (player.rect.topleft[0] // CELL, player.rect.topleft[1] // CELL)
    field = do_field(walls)
    graph = do_graph(field)

    if player_coord not in graph:
        return graph[enemy_coord][0]
    
    path = find_path(graph, enemy_coord, player_coord)
    move_coord = path[1]

    return move_coord


if __name__ == "__main__":
    walls = 1
    do_field(walls)

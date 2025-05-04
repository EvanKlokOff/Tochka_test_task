import sys
from typing import List, Dict, Tuple
import collections

# Константы для символов ключей и дверей
keys_char = {chr(i) for i in range(ord('a'), ord('z') + 1)}
doors_char = {k.upper() for k in keys_char}

ROBOT_START_CELL = "@"
FREE_CELL = "."
WALL_CELL = "#"

def get_all_robots_keys(data: List[List[str]])->Tuple[List[int],Dict[str, int]]:
    rows = len(data)
    cols = len(data[0])
    robots = []
    keys = set()
    index = 0
    #Ищем роботов и ключи
    for i in range(rows):
        for j in range(cols):
            if data[i][j] == ROBOT_START_CELL:
                robots.append((i,j))
            elif data[i][j] in keys_char:
                keys.add(data[i][j])
                index+=1
    return robots, keys

def solve(data: List[List[str]]) -> int:
    robots, available_keys = get_all_robots_keys(data)
    # доступные движения
    moves = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    # очередь, в которой будут хранится местоположения всех роботов, информация о собранных ключах, шагах, сделанных роботами
    queue = collections.deque()
    initial_state = (tuple(robots), frozenset(), 0)
    queue.append(initial_state)

    spent_states = set()
    spent_states.add(initial_state)

    while queue:
        robots, collected_keys, step = queue.popleft()
        if collected_keys == available_keys:
            return step

        # пробуем подвигать роботов
        for robot_index, robot in enumerate(robots):
            for move_x, move_y in moves:
                new_x, new_y = robot[0]+move_x, robot[1]+move_y
                cell = data[new_x][new_y]

                # проверяем можно ли сдвинуть робота по указанному направлению, если нельзя, то меняем направление
                if cell == WALL_CELL:
                    continue
                if cell in doors_char:
                    key = cell.lower()
                    if key not in collected_keys:
                        continue

                # если получилось сдвинуть робота, то смотрим, если на клетке ключ

                new_collected_keys = set(collected_keys)
                if cell in keys_char:
                    new_collected_keys.add(cell)
                new_collected_keys = frozenset(new_collected_keys)

                #делаем новое состояние и помещаем его в очередь
                new_robots = list(robots)
                new_robots[robot_index] = (new_x, new_y)
                new_state = (tuple(new_robots), new_collected_keys, step+1)

                if new_state not in spent_states:
                    spent_states.add(new_state)
                    queue.append(new_state)
    return -1

def get_input():
    """Чтение данных из стандартного ввода."""
    return [list(line.strip()) for line in sys.stdin]

def main():
    data = get_input()
    result = solve(data)
    print(result)


if __name__ == '__main__':
    main()

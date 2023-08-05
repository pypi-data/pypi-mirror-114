"""A pure Python, text-interface clone of the Laby game."""

import os
import random

Exit = 'Exit'
Rock = 'Rock'
Unknown = 'Unknown'
Void = 'Void'
Wall = 'Wall'
Web = 'Web'

RobotUp = 'RobotUp'
RobotDown = 'RobotDown'
RobotLeft = 'RobotLeft'
RobotRight = 'RobotRight'


STATE_MAP = {
    'o': Wall,
    'w': Web,
    '.': Void,
    'r': Rock,
    'x': Exit,
    '↑': RobotUp,
    '→': RobotRight,
    '←': RobotLeft,
    '↓': RobotDown
}

REVERSE_STATE_MAP = {value: key for key, value in STATE_MAP.items()}


class Controller:

    def __init__(self, level_map, position, orientation):
        self.original_level_map = level_map
        self.original_position = position
        self.original_orientation = orientation
        self.level_map = level_map.copy()
        self.position = position
        self.orientation = orientation
        self.holding = None
        self.stuck = False
        self.escaped = False
        self.visible = False

    def show(self):
        print()
        for line in self.to_map_lines():
            print(' '.join(line))
        if self.holding:
            print("Holding:", MANAGER.controller.holding)
        if self.stuck:
            print("Stuck!")
        if self.escaped:
            print("Escaped!")
        print()

    def reset(self):
        self.level_map = self.original_level_map.copy()
        self.position = self.original_position
        self.orientation = self.orientation
        self.holding = None
        self.stuck = False
        self.escaped = False

        if self.visible:
            self.show()

    def to_map_lines(self):
        min_x, min_y = max_x, max_y = self.position
        if self.level_map:
            min_x = min(min_x, min(x for x, y in self.level_map))
            min_y = min(min_y, min(y for x, y in self.level_map))
            max_x = max(max_x, max(x for x, y in self.level_map))
            max_y = max(max_y, max(y for x, y in self.level_map))
        lines = []
        for y in range(max_y, min_y - 1, -1):
            chars = []
            for x in range(min_x, max_x + 1):
                if (x, y) == self.position:
                    state = self.orientation
                else:
                    state = self.level_map.get((x, y), Void)
                chars.append(REVERSE_STATE_MAP[state])
            line = ''.join(chars)
            lines.append(line)
        return lines

    def next_position(self):
        x, y = self.position
        if self.orientation is RobotUp:
            return x, y + 1
        elif self.orientation is RobotDown:
            return x, y - 1
        elif self.orientation is RobotRight:
            return x + 1, y
        else:
            assert self.orientation is RobotLeft
            return x - 1, y

    def drop(self):
        if not self.holding:
            return "You're not holding anything."

        next_position = self.next_position()
        if self.level_map.get(next_position, Void) not in (Void, Web):
            return "There's something in the way."

        self.level_map[next_position] = self.holding
        self.holding = None

        if self.visible:
            self.show()

    def escape(self):
        if self.escaped:
            return "You've already escaped."
        if self.stuck:
            return "You're stuck."
        if self.holding:
            return "You can't take that with you."

        next_position = self.next_position()
        if self.level_map.get(next_position, Void) is not Exit:
            return "This is not an exit."

        del self.level_map[next_position]
        self.position = next_position
        self.escaped = True

        if self.visible:
            self.show()

    def forward(self):
        if self.stuck:
            return "You're stuck."

        next_position = self.next_position()
        next_state = self.level_map.get(next_position, Void)
        if next_state is Void:
            self.position = next_position
        elif next_state is Web:
            self.position = next_position
            self.stuck = True

        if self.visible:
            self.show()

    def left(self):
        if self.orientation is RobotLeft:
            self.orientation = RobotDown
        elif self.orientation is RobotDown:
            self.orientation = RobotRight
        elif self.orientation is RobotRight:
            self.orientation = RobotUp
        else:
            assert self.orientation is RobotUp
            self.orientation = RobotLeft

        if self.visible:
            self.show()

    def look(self):
        return self.level_map.get(self.next_position(), Void)

    def right(self):
        if self.orientation is RobotLeft:
            self.orientation = RobotUp
        elif self.orientation is RobotDown:
            self.orientation = RobotLeft
        elif self.orientation is RobotRight:
            self.orientation = RobotDown
        else:
            assert self.orientation is RobotUp
            self.orientation = RobotRight

        if self.visible:
            self.show()

    def take(self):
        if self.holding:
            return "You're already holding something."

        next_position = self.next_position()
        if self.level_map.get(next_position, Void) is not Rock:
            return "You can't pick this up."

        self.holding = self.level_map.pop(next_position)

        if self.visible:
            self.show()


class LevelGenerator:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.state_weights = {
            Rock: random.random(),
            Void: random.random(),
            Web: random.random()
        }
        self.direction_weights = {
            'forward': random.random(),
            'left': random.random(),
            'right': random.random(),
            'backward': random.random()
        }

    @staticmethod
    def weighted_random(weight_map):
        total = sum(weight_map.values())
        assert total > 0
        selector = random.uniform(0, total)
        for state, weight in weight_map.items():
            selector -= weight
            if selector <= 0:
                return state
        return random.choice(list(weight_map))

    def random_state(self):
        return self.weighted_random(self.state_weights)

    def iter_neighbors(self, position, margin=1):
        x, y = position
        if y < self.height - 1 - margin:
            yield x, y + 1
        if x < self.width - 1 - margin:
            yield x + 1, y
        if y > margin:
            yield x, y - 1
        if x > margin:
            yield x - 1, y

    def random_direction(self, available):
        if len(available) == 4:
            return self.weighted_random(self.direction_weights)
        else:
            return self.weighted_random({direction: weight
                                         for direction, weight in self.direction_weights.items()
                                         if direction in available})

    def random_neighbor(self, previous_position, current_position, visits):
        x1, y1 = previous_position
        x2, y2 = current_position
        x_delta = x2 - x1
        y_delta = y2 - y1
        assert abs(x_delta) in (0, 1) and abs(y_delta) in (0, 1) and abs(x_delta) != abs(y_delta)
        if y_delta == 1:
            movement_direction = 0
        elif x_delta == 1:
            movement_direction = 1
        elif y_delta == -1:
            movement_direction = 2
        else:
            assert x_delta == -1
            movement_direction = 3
        neighbors = [(x2, y2 + 1), (x2 + 1, y2), (x2, y2 - 1), (x2 - 1, y2)]
        neighbors = neighbors[movement_direction:] + neighbors[:movement_direction]
        assert neighbors[0] == (x2 + x_delta, y2 + y_delta)
        neighbor_map = {key: (x3, y3)
                        for key, (x3, y3) in zip(['forward', 'right', 'backward', 'left'],
                                                 neighbors)
                        if 0 < x3 < self.width - 1 and 0 < y3 < self.height - 1}
        assert neighbor_map, (neighbors, self.width, self.height)
        min_visit_count = min(visits.get(neighbor, 0) for neighbor in neighbor_map.values())
        available = {key for key, neighbor in neighbor_map.items()
                     if visits.get(neighbor, 0) == min_visit_count}
        new_direction = self.random_direction(available)
        return neighbor_map[new_direction]

    def generate_level(self):
        level_map = {}
        start_position = random.randrange(1, self.width - 1), random.randrange(1, self.height - 1)
        level_map[start_position] = Void
        visited = {start_position: 1}
        position = start_position
        x, y = position
        previous_position = random.choice([(x, y + 1), (x + 1, y), (x, y - 1), (x - 1, y)])
        has_rock = False
        has_web = False
        space = random.randint(2, (self.width - 2) * (self.height - 2))
        while len(level_map) < space:
            # min_visit_count = min(visited.get(neighbor, 0)
            #                       for neighbor in self.iter_neighbors(position))
            # least_visited = [neighbor for neighbor in self.iter_neighbors(position)
            #                  if visited.get(neighbor, 0) == min_visit_count]
            # position = random.choice(least_visited)
            previous_position, position = position, self.random_neighbor(previous_position,
                                                                         position, visited)
            if position not in level_map:
                state = self.random_state()
                if state is Web and not has_rock:
                    state = Rock
                level_map[position] = state
                if state is Rock:
                    has_rock = True
                elif state is Web:
                    has_web = True
            visited[position] = visited.get(position, 0) + 1
        assert has_rock or not has_web
        boundaries = {position for position in level_map
                      if (position != start_position and
                          sum(neighbor in level_map
                              for neighbor in self.iter_neighbors(position)) < 4)}
        assert boundaries
        least_visited_boundary = min(boundaries, key=visited.get)
        neighbors = [neighbor for neighbor in self.iter_neighbors(least_visited_boundary, margin=0)
                     if neighbor not in level_map]
        assert neighbors
        end_position = random.choice(neighbors)
        level_map[end_position] = Exit

        walls = set()
        voids = set()
        for x in range(self.width):
            for y in range(self.height):
                position = (x, y)
                if position not in level_map:
                    if any(neighbor in level_map for neighbor in self.iter_neighbors(position)):
                        walls.add(position)
                elif level_map[position] is Void:
                    voids.add(position)
        for position in walls:
            level_map[position] = Wall
        for position in voids:
            del level_map[position]

        orientation = random.choice([RobotUp, RobotRight, RobotDown, RobotLeft])
        return Controller(level_map, start_position, orientation)


class Manager:

    def __init__(self):
        self.path = None
        self.map_lines = None
        self.level_generator = LevelGenerator(10, 10)
        self.controller = Controller({}, (0, 0), RobotUp)

    def reset_level(self):
        self.controller.reset()

    def parse_level(self, map_lines=None):
        level_map = {}
        y = 0
        position = None
        orientation = None
        for line in map_lines or self.map_lines:
            choices = {}
            for x, char in enumerate(line):
                key = char.lower()
                is_choice = char.isupper()
                state = STATE_MAP[key]
                if state in (RobotUp, RobotDown, RobotLeft, RobotRight):
                    assert position is None
                    assert orientation is None
                    position = (x, y)
                    orientation = state
                    state = Void
                if is_choice:
                    assert state is not Void
                    if state in choices:
                        choices[state].append(x)
                    else:
                        choices[state] = [x]
                if state is not Void:
                    level_map[x, y] = state
            for state, columns in choices.items():
                if state is Web:
                    remove_count = 1
                elif state is Rock:
                    remove_count = len(columns) - 1
                else:
                    remove_count = random.randint(0, len(columns))
                to_remove = random.sample(columns, remove_count)
                for x in to_remove:
                    del level_map[x, y]
            y += 1
        if position is None or orientation is None:
            # TODO: Should we just randomize in this case?
            raise ValueError("No starting position indicated in map!")
        # Flip Y axis to align with traditional graph axis orientation
        max_y = max(y for x, y in level_map)
        level_map = {(x, max_y - y): state for (x, y), state in level_map.items()}
        position = (position[0], max_y - position[1])
        self.map_lines = tuple(map_lines)
        self.controller = Controller(level_map, position, orientation)
        return self.controller

    def load_level(self, path=None):
        path = path or self.path
        if path is None:
            raise RuntimeError("No map file path specified.")
        if not os.path.isfile(path):
            raise FileNotFoundError(path)
        map_lines = []
        in_map = False
        with open(path, encoding='utf-8') as file:
            for line_no, line in enumerate(file):
                line = line.rstrip()
                if line == 'map:':
                    in_map = True
                elif not line and in_map:
                    break
                elif in_map:
                    line = ''.join(line.split())
                    bad_chars = set(line.lower()) - STATE_MAP.keys()
                    if bad_chars:
                        raise ValueError("Unexpected map char(s) on line %s of %s: %r" %
                                         (line_no + 1, path, ''.join(sorted(bad_chars))))
                    map_lines.append(line)
        if not in_map or not map_lines:
            raise RuntimeError("File does not contain a valid map: %s" % path)
        self.path = path
        return map_lines

    def generate_level(self, width=10, height=10):
        level_generator = LevelGenerator(width, height)
        self.controller = level_generator.generate_level()
        self.map_lines = self.controller.to_map_lines()
        return self.map_lines


MANAGER = Manager()


def load_level(path=None):
    map_lines = MANAGER.load_level(path)
    MANAGER.parse_level(map_lines)


def generate_level(width=10, height=10):
    MANAGER.generate_level(width, height)


def drop():
    MANAGER.controller.drop()


def escape():
    MANAGER.controller.escape()


def forward():
    MANAGER.controller.forward()


def left():
    MANAGER.controller.left()


def look():
    return MANAGER.controller.look()


def right():
    MANAGER.controller.right()


def say(text):
    print(text)


def take():
    MANAGER.controller.take()


def show():
    MANAGER.controller.visible = True


def hide():
    MANAGER.controller.visible = False

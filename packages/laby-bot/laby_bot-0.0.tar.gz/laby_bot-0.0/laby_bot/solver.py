"""
This is a bot for solving levels in the educational programming game, "Laby". The goal of each level
in the game is to navigate an ant to an exit without getting caught by any big spider webs. The game
consists of 2D levels laid out in a square grid, where each square can be open space (possibly
containing invisible rubble or a small spider web), a wall, a rock, a big spider web, or the exit.
You are given certain primitive actions to work with: look at the contents of the square in front of
you, move forward to the square in front of you, turn left without moving forward, turn right
without moving forward, take a rock, drop the rock, say something, or escape through the exit in
front of you.

Laby can be installed from the Ubuntu Software Center. The source code is also available as a [git
repo](https://github.com/sgimenez/laby). See the [Laby homepage](https://sgimenez.github.io/laby/)
for more info. It would be exceedingly simple to clone the functionality in a pure Python module,
allowing for rapid evaluation of algorithms against a wide variety of levels. I plan to do so
eventually.

Copy and paste the code into the Laby code window and try it out on different levels. The bot works
by mapping out the level as it is explored, while searching for an exit. The fact that it constructs
an internal model of the world from its perceptions, rather than operating solely via
stimulus/response, means it is a proper AI by my own definition -- even if it is a relatively
trivial example of one.

The internal model construction algorithm assumes the correct topology of the environment, rather
than attempting to construct it from scratch. However, I think the basic algorithm here could be
extended to learn the topology from scratch by encoding each perception and each
location+orientation as a vector, each action as a matrix by which the current location+orientation
vector is to multiplied to predict the next location+orientation vector. The next
location+orientation vector would then be multiplied by another matrix to predict the perception
that would be observed from that location+orientation, if such an observation is made. Using
backpropagation, the location+orientation and perceptual prediction matrices could be trained to m
ake accurate predictions for perceptions observed from the current location+orientation and those
nearby (as measured in number of actions taken) in its neighborhood. This should result in the
system learning the approximate topology of the location+orientation space, thereby allowing an
approximate version of the below algorithm to be applied to properly explore the space to completion
as it currently does.

(For the specific case of this game, moving to a new level would require throwing away and
relearning the matrix that maps from location+orientation to perception, while preserving the
matrices that are used to update location+orientation. In other words, the perceptual matrix
corresponds to the level_map in the Navigator class below, which is level-specific, whereas the
location+orientation update matrices correspond to the transformations applied by the
next_position() and turn() methods of that class, which are fixed from one level to the next. The
current location+orientation vector corresponds to the x, y, moving, and looking member variables of
that class, which are also reset to fixed initial values when moving to new levels.)

I believe that the ability to learn the topology of the environment and the transformations of
position within this topology effected by each available action is core to implementing AGI. It is
this flexibility in learning topological structures and transformations in the environment which
will ultimately distinguish general AI from narrow AI. Once a model of the environment and the
available actions upon it has been constructed, the rest just amounts to search and naive
optimization over this model.
"""


from laby_bot.robot import *


def sign(value):
    return 1 if value >= 0 else -1


class Solver:

    def __init__(self):
        self.level_map = {}
        self.x = 0
        self.y = 0
        self.moving = 0
        self.looking = 0
        self.carrying_rock = False
        self.level_map[self.x, self.y] = Void
        self.visited = {(self.x, self.y): 1}
        self.last_explored_position = (self.x, self.y)

    def current_position(self):
        return self.x, self.y

    def next_position(self, direction=0, from_position=None):
        if from_position is None:
            x, y = self.x, self.y
        else:
            x, y = from_position
        abs_direction = (self.moving + direction) % 4
        if abs_direction == 0:
            return x + 1, y
        elif abs_direction == 1:
            return x, y + 1
        elif abs_direction == 2:
            return x - 1, y
        else:
            assert abs_direction == 3
            return x, y - 1

    def turn(self, direction):
        direction %= 4
        if self.looking == direction:
            pass
        elif self.looking == (direction + 1) % 4:
            right()
        elif self.looking == (direction - 1) % 4:
            left()
        else:
            assert self.looking == (direction + 2) % 4
            left()
            left()
        self.looking = direction

    def look(self, direction=0, refresh=False):
        position = self.next_position(direction)
        if not refresh and position in self.level_map:
            return self.level_map[position]
        self.turn(direction)
        seen = look()
        self.level_map[position] = seen
        return seen

    def move(self, direction=0):
        self.turn(direction)
        self.moving += direction
        self.moving %= 4
        self.looking = 0
        position = self.next_position()
        self.x, self.y = position
        forward()
        if position in self.visited:
            self.visited[position] += 1
        else:
            self.visited[position] = 1
            self.last_explored_position = position

    def take(self, direction=0):
        if not self.carrying_rock and self.look(direction) == Rock:
            self.turn(direction)
            take()
            self.level_map[self.next_position(direction)] = Void
            self.carrying_rock = True
            return True
        else:
            return False

    def drop(self, direction=0):
        if self.carrying_rock and self.look(direction) == Void:
            self.turn(direction)
            drop()
            self.level_map[self.next_position(direction)] = Rock
            self.carrying_rock = False
            return True
        else:
            return False

    def drop_and(self, action):
        original = self.looking
        if self.carrying_rock:
            for direction in range(4):
                if direction != original and self.drop(direction):
                    break
        self.turn(original)
        return action()

    def clear(self, direction=0):
        if self.carrying_rock and self.look(direction) == Web:
            self.turn(direction)
            drop()
            take()
            self.level_map[self.next_position(direction)] = Void
            return True
        else:
            return False

    def get_neighborhood(self, from_position=None):
        neighborhood = []
        for direction in range(4):
            neighbor_position = self.next_position(direction, from_position)
            neighborhood.append(self.level_map.get(neighbor_position, None))
        return neighborhood

    def iter_unvisited(self, states=None):
        for position in self.visited:
            for direction in range(4):
                neighbor_position = self.next_position(direction, position)
                if neighbor_position not in self.visited and \
                        self.level_map.get(neighbor_position, None) in states:
                    yield neighbor_position

    def distance_to(self, position, from_position=None):
        x_stop, y_stop = position
        x_start, y_start = from_position or (self.x, self.y)
        return abs(x_stop - x_start) + abs(y_stop - y_start)

    def directions_to(self, position):
        return sorted(range(4),
                      key=lambda direction: ((self.visited.get(self.next_position(direction),
                                                               0) + 1) *
                                             self.distance_to(position,
                                                              self.next_position(direction))))

    def run(self):
        while True:
            self.look()

            if self.carrying_rock:
                preferences = (Exit, Web, Void, Rock, Unknown, None)
            else:
                preferences = (Exit, Void, Rock, Unknown, None)

            unvisited = set(self.iter_unvisited(preferences))
            if not unvisited:
                say("I'm trapped!")
                return

            nearest = min(unvisited,
                          key=lambda position: (
                                  self.distance_to(position) *
                                  self.distance_to(position, self.last_explored_position)
                          ))
            # say("Nearest distance: %s" % (navigator.distance_to(nearest),))
            for direction in self.directions_to(nearest):
                seen = self.look(direction)
                if seen == Exit:
                    say("Aha!")
                    self.turn(direction)
                    self.drop_and(escape)
                    return
                elif seen in (Void, Unknown):
                    self.move(direction)
                    break
                elif seen == Rock:
                    if self.carrying_rock:
                        say("Hmm...")
                    self.turn(direction)
                    assert self.drop_and(lambda: self.take(direction))
                    self.move(direction)
                    break
                elif self.carrying_rock and seen == Web:
                    self.clear(direction)
                    say("Ha!")
                    self.move(direction)
                elif seen != Wall:
                    say("Nope!")


def run():
    solver = Solver()
    solver.run()

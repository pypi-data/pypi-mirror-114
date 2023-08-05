# Laby Bot
*A pure Python, text-interface clone and solver of the Laby game*

## What's it for?

This package has a couple of purposes:

* To demonstrate how *modeling* the environment makes it easy to implement 
  planning and reasoning.
* To provide a useful toy problem for testing out other AI algorithms.

## Installation

Laby Bot can be installed by the command:

`pip install laby_bot`

**NOTE**: The modules will still work, but some of the tests will fail without 
the original Laby levels. You'll need to create a symlink to them. You can 
find them [here](https://github.com/sgimenez/laby/tree/master/data/levels).

## Quick Start

### Playing the Game

The `laby_bot.robot` submodule is intended as a drop-in replacement for the 
`robot` module of the original Laby game. You can test your bot code out on a
given level like this:

```python3
from laby_bot.robot import *

load_level('<path to laby level>.laby')
show()

# Paste your bot code here, minus the "from robot import *" line
# that would normally appear at the top. All the standard robot
# instructions available in the Laby game are provided. 
```

When you run the above code, the map will be printed out to the command line 
after each move is taken by your bot.

### Running the Solver

The `laby_bot.solver` submodule contains a generic solver for any (solvable)
Laby level. You can test it out on a randomly generated level like this:

```python3
from laby_bot.robot import generate_level, show
from laby_bot.solver import run

generate_level()
show()
run()
```

Or you can simply run it from the command line:

`python3 -m laby_bot`

from laby_bot.solver import run
from laby_bot.robot import show, generate_level


def main():
    generate_level()
    show()
    run()

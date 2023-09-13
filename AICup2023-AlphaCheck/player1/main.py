import procode.p1 as p1
from src.components.client_game import ClientGame

flag = False


def initializer(game: ClientGame):
    p1.initializer(game)

def turn(game: ClientGame):
    p1.turn(game)
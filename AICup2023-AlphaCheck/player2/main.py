import procode.p2 as p2
from src.components.client_game import ClientGame

flag = False


def initializer(game: ClientGame):
    p2.initializer(game)

def turn(game: ClientGame):
    p2.turn(game)
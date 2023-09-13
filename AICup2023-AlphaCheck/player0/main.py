import procode.p0 as p0
from src.components.client_game import ClientGame

flag = False


def initializer(game: ClientGame):
    p0.initializer(game)

def turn(game: ClientGame):
    p0.turn(game)
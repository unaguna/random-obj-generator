import randog.factory


def _implementation():
    raise Exception("error for test")


FACTORY = randog.factory.by_callable(_implementation)

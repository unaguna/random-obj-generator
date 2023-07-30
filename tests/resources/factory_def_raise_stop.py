import randog.factory


def _implementation():
    raise StopIteration()


FACTORY = randog.factory.by_callable(_implementation)

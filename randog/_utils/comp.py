class _AnywayMaximum:
    def __eq__(self, other):
        return self.__class__ == other.__class__

    def __le__(self, other):
        return self == other

    def __lt__(self, other):
        return False

    def __ge__(self, other):
        return True

    def __gt__(self, other):
        return self != other


ANYWAY_MAXIMUM = _AnywayMaximum()

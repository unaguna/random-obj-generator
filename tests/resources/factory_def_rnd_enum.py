import enum
import randog


class MyEnum(enum.Enum):
    one = 1
    two = 2
    three = 3


FACTORY = randog.factory.randenum(MyEnum)

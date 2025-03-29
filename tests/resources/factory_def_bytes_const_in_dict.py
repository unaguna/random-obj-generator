import randog.factory

FACTORY = randog.factory.randdict(
    int=randog.factory.randint(1, 1),
    str=randog.factory.randstr(length=3, charset="a"),
    bytes=randog.factory.const(b"\x40\x88\xff"),
)

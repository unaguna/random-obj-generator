import randog.factory

FACTORY = randog.factory.randlist(
    randog.factory.const(1),
    randog.factory.randstr(length=3, charset="a"),
    randog.factory.const(b"\x40\x88\xff"),
)

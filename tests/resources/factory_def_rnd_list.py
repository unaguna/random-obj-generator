import randog

FACTORY = randog.factory.randlist(
    randog.factory.randint(0, 100),
    randog.factory.randstr(),
    randog.factory.randbool(),
    length=randog.factory.randint(0, 3),
)

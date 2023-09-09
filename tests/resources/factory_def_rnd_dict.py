import randog

FACTORY = randog.factory.randdict(
    a=randog.factory.randint(0, 100),
    b=randog.factory.randstr(),
    c=randog.factory.randbool(),
)

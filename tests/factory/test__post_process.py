import randog.factory


def test__post_process():
    factory = randog.factory.randint(10, 10).post_process(lambda x: str(x))
    generated = factory.next()

    assert generated == "10"


def test__post_process__none():
    factory = randog.factory.randint(10, 10).post_process(lambda x: str(x)).or_none(1.0)
    generated = factory.next()

    assert generated is None


def test__post_process__none2():
    factory = randog.factory.randint(10, 10).or_none(1.0).post_process(lambda x: str(x))
    generated = factory.next()

    assert generated == "None"

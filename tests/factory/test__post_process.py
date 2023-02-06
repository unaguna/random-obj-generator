import ranog.factory


def test_post_process():
    factory = ranog.factory.randint(10, 10).post_process(lambda x: str(x))
    generated = factory.next()

    assert generated == "10"


def test_post_process__none():
    factory = ranog.factory.randint(10, 10).post_process(lambda x: str(x)).or_none(1.0)
    generated = factory.next()

    assert generated is None


def test_post_process__none2():
    factory = ranog.factory.randint(10, 10).or_none(1.0).post_process(lambda x: str(x))
    generated = factory.next()

    assert generated == "None"

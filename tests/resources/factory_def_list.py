import datetime
import itertools

import randog.factory

CONST_DATE = datetime.date(2019, 10, 14)

items = [
    randog.factory.by_iterator(itertools.count(0)),
    randog.factory.randstr(length=3, charset="a"),
    randog.factory.randdate(CONST_DATE, CONST_DATE),
]

FACTORY = randog.factory.randlist(*items)

import datetime
import itertools

import randog.factory

CONST_DATE = datetime.date(2019, 10, 14)

items = {
    "id": randog.factory.by_iterator(itertools.count(0)),
    "name": randog.factory.randstr(length=3, charset="a"),
    "join_date": randog.factory.randdate(CONST_DATE, CONST_DATE),
}

FACTORY = randog.factory.randdict(**items)

import itertools

import randog.factory

items = {
    "id": randog.factory.by_iterator(itertools.count(0)),
    "name": randog.factory.randstr(length=3, charset="a"),
    "join_datetime": randog.factory.randdatetime(),
}

CSV_COLUMNS = list(items.keys())

FACTORY = randog.factory.randdict(**items)

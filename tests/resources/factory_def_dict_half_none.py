import datetime
import itertools

import randog.factory

CONST_DATE = datetime.date(2019, 10, 14)

items = {
    "id": randog.factory.by_iterator(itertools.count(0)),
    "name": randog.factory.randstr(length=3, charset="a"),
    "join_date": randog.factory.randdate(CONST_DATE, CONST_DATE),
}

CSV_COLUMNS = list(items.keys())


def post_process(value):
    post_process.count += 1
    if post_process.count % 2 != 0:
        return value
    else:
        return None


post_process.count = 0


FACTORY = randog.factory.randdict(**items).post_process(post_process)

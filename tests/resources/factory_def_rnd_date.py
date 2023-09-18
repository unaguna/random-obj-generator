from datetime import date
import randog

FACTORY = randog.factory.randdate(
    date(2023, 2, 1),
    date(2024, 2, 1),
)

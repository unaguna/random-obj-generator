from datetime import time
import randog

FACTORY = randog.factory.randtime(
    time(1),
    time(10),
)

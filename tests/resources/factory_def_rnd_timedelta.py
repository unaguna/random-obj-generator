from datetime import timedelta
import randog

FACTORY = randog.factory.randtimedelta(timedelta(0), timedelta(hours=12))

import os
import randog.factory

FACTORY = randog.factory.const(os.environ.get("VALUE", "_default"))

**randog 0.1.0.x — Randomly object generator**

**randog** is a package which helps to generate data randomly.

For example:

```python
import uuid
import randog.factory

factory = randog.factory.from_example({"uuid": uuid.uuid4, "name": "", "age": 20})
generated = factory.next()

assert isinstance(generated, dict)
assert isinstance(generated["uuid"], uuid.UUID)
assert isinstance(generated["name"], str)
assert isinstance(generated["age"], int)
```

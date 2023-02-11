**ranog 0.1.0.x — Randomly object generator**

**ranog** is a package which helps to generate data randomly.

For example:

```python
import uuid
import ranog.factory

factory = ranog.factory.from_example({"uuid": uuid.uuid4, "name":"", "age": 20})
generated = factory.next()

assert isinstance(generated, dict)
assert isinstance(generated["uuid"], uuid.UUID)
assert isinstance(generated["name"], str)
assert isinstance(generated["age"], int)
```

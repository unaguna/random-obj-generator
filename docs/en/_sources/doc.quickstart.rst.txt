Quick start
===========

You can try randog by following these steps.


Installation
------------

Prepare python 3.8 or newer and install randog using the pip command as follows:

.. code-block:: shell

   pip install randog

Minimal use (as command)
------------------------

randog can be executed as a command. Here is an example of one of the simplest command executions:

.. code-block:: shell

    randog str

For other uses of command execution, please refer to :doc:`doc.as_command`.

Minimal use (in programs)
-------------------------

By passing an example of the object you want to generate to the :code:`from_example` function, you can create a factory that randomly generates objects.

.. doctest::

   >>> import uuid
   >>> import randog.factory

   >>> factory = randog.factory.from_example({"uuid": uuid.uuid4, "name": "", "age": 20})
   >>> generated = factory.next()

   >>> assert isinstance(generated, dict)
   >>> assert isinstance(generated["uuid"], uuid.UUID)
   >>> assert isinstance(generated["name"], str)
   >>> assert isinstance(generated["age"], int)


This example generates a dict object, but it can also generate a list, just str, etc.

byfile Mode
===========

In byfile mode, values are generated using the factories defined in :doc:`a factory definition <doc.external_def>`. An example run is as follows:

.. code-block:: shell

    python -m randog byfile factory_def.py

The argument :code:`factory_def.py` is :doc:`a filename of the factory definition <doc.external_def>`. It must be python code that creates an instance of factory in the variable FACTORY as in the following example:

.. code-block:: python

    import uuid

    FACTORY = randog.factory.from_example({
        "uuid": uuid.uuid4,
        "name": "",
        "age": 20,
    })

.. note::
    In factory definition file, :code:`import randog` can be omitted.

Arguments and Options
---------------------

No unique arguments.

Common options are available; see also :doc:`doc.as_command.common_option`

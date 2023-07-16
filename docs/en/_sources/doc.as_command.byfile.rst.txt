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


Examples
--------

The simplest example is the following:

.. code-block:: shell

    python -m randog byfile factory_def.py

If the definition file defines a factory that generates a dict equivalent to one record in the database, you can obtain data for testing by generating multiple dict as shown below:

.. code-block:: shell

    # Generate list which contains 10 values
    python -m randog byfile factory_def.py -L 10

You may want to generate multiple values while outputting each one to a separate file. In that case, you can utilize :code:`-O` and :code:`-r` as follows:

.. code-block:: shell

    # Repeat 10 times and output each of them into out_001.json, out_002.json, ... with json format
    python -m randog byfile factory_def.py -r 10 -O 'out_{:03}.json' --json


byfile Mode
===========

In byfile mode, values are generated using the factories defined in :doc:`a factory definition <doc.external_def>`. The format of the command is as follows:

.. code-block:: shell

    randog byfile FACTORY_PATH [...] [--regenerate PROB_REGEN] [--discard PROB_DISCARD] [--csv ROW_NUM] [--error-on-factory-stopped] [common-options]

The argument FACTORY_PATH is :doc:`a filename of the factory definition <doc.external_def>`. It must be python code that creates an instance of factory in the variable FACTORY as in the following example:

.. code-block:: python

    import uuid

    FACTORY = randog.factory.from_example({
        "uuid": uuid.uuid4,
        "name": "",
        "age": 20,
    })

    # (optional) Settings used for CSV output
    CSV_COLUMNS = ["uuid", "name", "age"]

.. note::
    In factory definition file, :code:`import randog` can be omitted.


Arguments and Options
---------------------

- :code:`FACTORY_PATH [...]`:

    - paths of one or more :doc:`factory definition files <doc.external_def>`.

- :code:`--regenerate PROB_REGEN` (default=0.0):

    - the probability that the factory generation value is not returned as is, but is regenerated. It affects cases where the original factory returns a value that is not completely random.

- :code:`--discard PROB_DISCARD` (default=0.0):

    - the probability that the factory generation value is not returned as is, but is discarded. If discarded, the number of times the value is generated is less than :code:`--repeat/-r` or :code:`--list/-L` or :code:`--csv`.

- :code:`--csv ROW_NUM` (optional):

    - if specified, it outputs generated ROW_NUM objects as CSV. When using this option, it is recommended to use a factory that generates dictionaries and to define :code:`CSV_COLUMNS` in the definition file to specify the fields of the CSV.

- :code:`--error-on-factory-stopped` (optional):

    - If specified, error is occurred in case the factory cannot generate value due to `StopIteration <https://docs.python.org/3/library/exceptions.html#StopIteration>`_. If not specified, the generation simply stops in the case.

- :code:`common-options`

    - :doc:`common options <doc.as_command.common_option>`


Examples
--------

The simplest example is the following:

.. code-block:: shell

    randog byfile factory_def.py

If the definition file defines a factory that generates a dict equivalent to one record in the database, you can obtain data for testing by generating multiple dict as shown below:

.. code-block:: shell

    # Generate list which contains 10 values
    randog byfile factory_def.py -L 10

You may want to generate multiple values while outputting each one to a separate file. In that case, you can utilize :code:`-O` and :code:`-r` as follows:

.. code-block:: shell

    # Repeat 10 times and output each of them into out_001.json, out_002.json, ... with json format
    randog byfile factory_def.py -r 10 -O 'out_{:03}.json' --json

You may want to discard some of the generated values, for example, if you are using PK with missing some timestamps.
In the case, the output can be made missing by :code:`--discard` or :code:`--regenerate`. For example:

.. code-block:: shell

    # output at most 20 values (each value will be discarded at 10% probability)
    randog byfile factory_def.py --repeat 20 --discard 0.1

    # output exactly 20 values (each value will be regenerated at 10% probability)
    randog byfile factory_def.py --repeat 20 --regenerate 0.1


.. _output_as_csv:

output as CSV
~~~~~~~~~~~~~

To output in CSV format, use the :code:`--csv` option. The value of each field is determined by the :code:`CSV_COLUMNS` defined in the definition file.

.. code-block:: shell

    # output CSV which contains 20 rows
    randog byfile factory_def.py --csv 20

.. warning::
    Even if factory generates objects other than dict or :code:`CSV_COLUMNS` is not defined in the definition file, it will output something in CSV format if the :code:`--csv` option is specified, but this is not recommended. This behavior may be changed in the future.

CSV output can also be output to multiple files with the :code:`--repeat/-r` and :code:`--output/-O` options.
In the following example, it outputs 20 lines to each of 10 CSV files.

.. code-block:: shell

    # output 10 CSV files; each file contains 20 rows
    randog byfile factory_def.py --csv 20 -r 10 -O 'out_{:03}.csv'

In the example at the top of this page, :code:`CSV_COLUMNS` was defined as a list of strings, but you can also specify a function that returns a field instead of a string that specifies a dictionary key.
In the following example, the third field is a string that is processed from the value of age.

.. code-block:: python

    import uuid

    FACTORY = randog.factory.from_example({
        "uuid": uuid.uuid4,
        "name": "",
        "age": 20,
    })

    # output example: 17642547-0a4c-4897-a8da-2d495558b8fa,d40s8Jqs,20 years old
    CSV_COLUMNS = [
        "uuid",
        "name",
        lambda d: f"{d['age']} years old",
    ]

You may want to discard some of the generated values, for example, if you are using PK with missing some timestamps.
In the case, the output can be made missing by :code:`--discard` or :code:`--regenerate`. For example:

.. code-block:: python

    import uuid
    from datetime import datetime, timedelta
    import randog

    def timestamp_iter():
        next = datetime(2002, 1, 1, 0)
        while True:
            yield next
            next += timedelta(hours=1)

    FACTORY = randog.factory.randdict(
        timestamp=randog.factory.by_iterator(timestamp_iter()),
        name=randog.factory.randstr(),
        age=randog.factory.randint(0, 100),
    )

    CSV_COLUMNS = ["timestamp", "name", "age"]

.. code-block:: shell

    # output at most 20 rows (each row will be discarded at 10% probability)
    randog byfile factory_def.py --csv 20 --discard 0.1

    # output exactly 20 rows (Gaps of 'timestamp' at 10% probability)
    randog byfile factory_def.py --csv 20 --regenerate 0.1

.. note::
    Missing rows by :code:`--discard` will result in fewer rows of output than the number specified by :code:`--csv`.

.. note::
    Skipping rows by :code:`--regenerate` will result in higher generations than the number specified by :code:`--csv`.


Change behavior patterns by environment variables
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

One useful idea is to allow the detailed settings of the factory definition to be changed by environment variables. For example, the following definition file allows the initial value of :code:`id` to be specified by an environment variable.

.. code-block:: python

    import itertools
    import os
    import randog

    initial_id = int(
        os.environ.get("INIT_ID", "0")
    )

    FACTORY = randog.factory.randdict(
        id=randog.factory.by_iterator(itertools.count(initial_id)),
        name=randog.factory.randstr(),
        age=randog.factory.randint(0, 100),
    )

In addition to the standard shell method, the env option of randog can be used to specify environment variables. All of the following examples work the same way:

.. code-block:: shell

    # Can use it in bash, etc., but not in powershell
    INIT_ID=5 randog byfile factory_def.py

    # Can use it in any shell
    randog byfile factory_def.py --env INIT_ID=5

.. note::
    Multiple environment variables can also be specified as follows:

    .. code-block:: shell

        randog byfile factory_def.py --env INIT_ID=5 VAR=foo
        randog byfile factory_def.py --env INIT_ID=5 --env VAR=foo

.. note::

    If you want to make the definition file importable, it may be better to implement the reading of environment variables in :code:`if __name__ == "__randog__"`. See :ref:`importable_definition_files` for details.

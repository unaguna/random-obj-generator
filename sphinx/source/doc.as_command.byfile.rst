byfile Mode
===========

In byfile mode, values are generated using the factories defined in :doc:`a factory definition <doc.external_def>`. The format of the command is as follows:

.. code-block:: shell

    python -m randog byfile FACTORY_PATH [...] [--csv ROW_NUM] [common-options]

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

- :code:`--csv ROW_NUM` (optional):
    -  if specified, it outputs generated ROW_NUM objects as CSV. When using this option, it is recommended to use a factory that generates dictionaries and to define :code:`CSV_COLUMNS` in the definition file to specify the fields of the CSV.

- :code:`common-options`
    - :doc:`common options <doc.as_command.common_option>`


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


output as CSV
~~~~~~~~~~~~~

To output in CSV format, use the :code:`--csv` option. The value of each field is determined by the :code:`CSV_COLUMNS` defined in the definition file.

.. code-block:: shell

    # output CSV which contains 20 rows
    python -m randog byfile factory_def.py --csv 20

.. warning::
    Even if factory generates objects other than dict or :code:`CSV_COLUMNS` is not defined in the definition file, it will output something in CSV format if the :code:`--csv` option is specified, but this is not recommended. This behavior may be changed in the future.

CSV output can also be output to multiple files with the :code:`--repeat/-r` and :code:`--output/-O` options.
In the following example, it outputs 20 lines to each of 10 CSV files.

.. code-block:: shell

    # output 10 CSV files; each file contains 20 rows
    python -m randog byfile factory_def.py --csv 20 -r 10 -O 'out_{:03}.csv'

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
In the case of CSV output, the output can be made missing by generating None.
In the following example, some records are missing by randomly converting the generated values to None.

.. code-block:: python

    import uuid
    from datetime import datetime, timedelta
    import random

    def timestamp_iter():
        next = datetime(2002, 1, 1, 0)
        while True:
            yield next
            next += timedelta(hours=1)

    # Returns None with 10% probability
    def post_process(value):
        if random.random() < 0.9:
            return value
        else:
            return None

    # The action of post_process causes this factory to ignore records generated with a probability of 10% and then return None.
    FACTORY = randog.factory.randdict(
        timestamp=randog.factory.by_iterator(timestamp_iter()),
        name=randog.factory.randstr(),
        age=randog.factory.randint(0, 100),
    ).post_process(post_process)

    CSV_COLUMNS = ["timestamp", "name", "age"]

.. code-block:: shell

    # output at most 20 rows
    python -m randog byfile factory_def.py --csv 20

.. note::
    Missing rows in this way will result in fewer rows of output than the number specified by :code:`--csv`.

.. warning::
    Using or_none or union as a means of generating None probabilistically does not allow for random missing. This is because a factory built using them first determines if it will output None, and generates a dict only if it does not.

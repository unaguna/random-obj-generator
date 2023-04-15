Run as Command
==============

randog can be used as a command. The simplest way to execute the command is as follows:

.. code-block:: shell

    python -m randog <factory_definition_file>

The argument is a filename of a factory definition and must be python code that creates an instance of factory in the variable FACTORY as in the following example:

.. code-block:: python

    FACTORY = randog.factory.from_example({
        "uuid": uuid.uuid4,
        "name": "",
        "age": 20,
    })

.. note::
    In factory definition file, :code:`import randog` can be omitted.


Output format
-------------

Normally, the generated objects are output as is with :code:`print()`, but the output format can be changed by using the following options.

- :code:`--repr`: The generated object is converted by using :code:`repr()` before output.
- :code:`--json`: Outputs the generated object in JSON format. Objects for which no standard JSON format is defined are converted to JSON after being converted to strings with :code:`str()`.

For example:

.. code-block:: shell

    python -m randog factory_def.py --json
    python -m randog factory_def.py --repr


Output to file
--------------

:code:`--output` option can be used to output to a file, as in the following example.

.. code-block:: shell

    python -m randog factory_def.py --output ./out.txt

.. note::
    The above example is not very practical, since the same thing can be done using the standard redirection feature of shell. This option exists to be combined with the other options described below. Details will be included when describing them.


Iteration
---------

There are two types of repeat generation options: :code:`--list` (:code:`-L`) and :code:`--repeat` (:code:`-r`).

If you want to output repeatedly generated objects in a single list, use :code:`--list` as follows:

.. code-block:: shell

    # generate ONE list which contains 3 objects; each element conforms to factory_def.py.
    python -m randog factory_def.py --list 3

On the other hand, if you want to output each repeatedly generated object separately, use :code:`--repeat` as follows:

.. code-block:: shell

    # generate and output 3 times
    python -m randog factory_def.py --repeat 3

.. note::
    If you want to output to different files one at a time using :code:`--repeat`, use :code:`--output` with a placeholder as follows:

    .. code-block:: shell

        # output to 'out_1.txt', 'out_2.txt', and 'out_3.txt'
        python -m randog factory_def.py --repeat 3 --output './out_{}.txt'

        # output to 'out_0001.txt', 'out_0002.txt', and 'out_0003.txt'
        python -m randog factory_def.py --repeat 3 --output './out_{:04}.txt'

    The rules for placeholders are the same as `the standard python format <https://docs.python.org/3/library/string.html#format-string-syntax>`_.

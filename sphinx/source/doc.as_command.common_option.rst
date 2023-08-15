Common Options
==============

Several options for command execution are available in all modes.

Output format
-------------

Normally, the generated objects are output as is with :code:`print()`, but the output format can be changed by using the following options.

- :code:`--repr`: The generated object is converted by using :code:`repr()` before output.
- :code:`--json`: Outputs the generated object in JSON format. Objects for which no standard JSON format is defined are converted to JSON after being converted to strings with :code:`str()`.

For example:

.. code-block:: shell

    python -m randog time --json
    python -m randog time --repr


.. _output_file:

Output to file
--------------

:code:`--output` option can be used to output to a file, as in the following example.

.. code-block:: shell

    python -m randog time --output ./out.txt

    # {now} will be replaced by the current time
    python -m randog time --output ./out_{now:%Y%m%d%H%M%S}.txt

As the example above also uses {now}, the following placeholders can be used with `format specification <https://docs.python.org/3/library/string.html#format-string-syntax>`_.

- :code:`{0}` (int):
    Serial number, which is a sequential number when the :code:`--repeat` option is used or when multiple definition files are used in order in byfile mode. If used only once, :code:`{}` is also acceptable.

- :code:`{def_file}` (str):
    The name of the definition file used in byfile mode; however, the trailing .py is removed. It is replaced by an empty string except in byfile mode.

- :code:`{repeat_count}` (int):
    Sequential numbers for repeating with the :code:`--repeat` option. If :code:`--repeat` is not used, it is replaced by 0.

- :code:`{factory_count}` (int):
    Sequential number assigned to each definition file when using multiple definition files in byfile mode. If in except in byfile mode, it is replaced by 0.

- :code:`{now}` (datetime.datetime):
    Current datetime.


As following example, You can specify the encoding and newline character for output with options :code:`--output-encoding` (:code:`-X`) and :code:`--output-linesep` (:code:`--O-ls`).

.. code-block:: shell

    # output to out.txt in UTF-16 LE with line-separator '\r\n'
    python -m randog byfile ./factory_def.py -O out.txt -X utf_16_le --O-ls CRLF


.. _iteration:

Iteration
---------

There are two types of repeat generation options: :code:`--list` (:code:`-L`) and :code:`--repeat` (:code:`-r`).

If you want to output repeatedly generated objects in a single list, use :code:`--list` as follows:

.. code-block:: shell

    # generate ONE list which contains 3 objects; each element conforms to factory_def.py.
    python -m randog byfile factory_def.py --list 3

On the other hand, if you want to output each repeatedly generated object separately, use :code:`--repeat` as follows:

.. code-block:: shell

    # generate and output 3 times
    python -m randog byfile factory_def.py --repeat 3

.. note::
    If you want to output to different files one at a time using :code:`--repeat`, use :code:`--output` with a placeholder as follows:

    .. code-block:: shell

        # output to 'out_1.txt', 'out_2.txt', and 'out_3.txt'
        python -m randog factory_def.py --repeat 3 --output './out_{}.txt'

        # output to 'out_0001.txt', 'out_0002.txt', and 'out_0003.txt'
        python -m randog factory_def.py --repeat 3 --output './out_{:04}.txt'

    The rules for placeholders are the same as `the standard python format <https://docs.python.org/3/library/string.html#format-string-syntax>`_.

    See :ref:`output_file` for available placeholders.


Modify environment variable
---------------------------

In particular, in byfile mode, you may want to specify environment variables for the purpose of passing values to the definition file. In bash and other shells, you can specify environment variables on a single line, such as :code:`VAR=VAL python -m randog ...`, but this is not possible in some shells, such as powershell.

Therefore, randog provides an option to specify environment variables. You can specify environment variables by using :code:`--env` as follows:

.. code-block:: shell

    python -m randog byfile factory_def.py --env CHARSET=0123456789abcdef

The above mentioned execution is useful, for example, when using a definition file such as the following:

.. code-block:: python

    import os
    import randog.factory

    FACTORY = randog.factory.randstr(
        length=4,
        # Get the value specified for charset from an environment variable
        charset=os.environ["CHARSET"],
    )

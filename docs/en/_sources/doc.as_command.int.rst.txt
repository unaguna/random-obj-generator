int Mode
========

In int mode, integer values are generated. The format of the command is as follows:

.. code-block:: shell

    python -m randog int MINIMUM MAXIMUM [--fmt FORMAT] [common-options]


Arguments and Options
---------------------

- :code:`MINIMUM`:

    - the minimum value.

- :code:`MAXIMUM`:

    - the maximum value.

- :code:`--fmt FORMAT` (optional):

    - the output format written in `format specification mini-language <https://docs.python.org/3/library/string.html?highlight=string#format-specification-mini-language>`_

- :code:`common-options`

    - :doc:`common options <doc.as_command.common_option>`


Examples
--------

The simplest example is the following, which outputs a value in the specified range.

.. code-block:: shell

    python -m randog int 0 100

.. note::

    If you want to generate decimal values, use :doc:`decimal mode <doc.as_command.decimal>` or :doc:`float mode <doc.as_command.float>`.

Format: 0-padding, etc.
~~~~~~~~~~~~~~~~~~~~~~~

The output format can be specified in `format specification mini-language <https://docs.python.org/3/library/string.html?highlight=string#format-specification-mini-language>`_ as follows:

.. code-block:: shell

    # output 0-padded integer such as '00000042'
    python -m randog int 0 100 --fmt 08

    # output 0-padded integer such as '+42'
    python -m randog int 0 100 --fmt +

Repeatedly Generate
~~~~~~~~~~~~~~~~~~~

Most likely, you will not be satisfied with just one generated, so you will probably want to output multiple times as follows:

.. code-block:: shell

    # Repeat 10 times
    python -m randog int -r 10

    # Generate list which contains 10 values
    python -m randog int -L 10

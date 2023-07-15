str Mode
========

In str mode, string values are generated. The format of the command is as follows:

.. code-block:: shell

    python -m randog str [--length LENGTH] [--charset CHARSET] [common-options]


Arguments and Options
---------------------

- :code:`--length LENGTH`:
    - the length of generated strings. You can specify an integer such as :code:`--length 5` or a range such as :code:`--length 3:8`.

- :code:`--charset CHARSET`:
    - the characters which contained by generated strings.

- :code:`common-options`
    - :doc:`common options <doc.as_command.common_option>`


Examples
--------

The simplest example is the following:

.. code-block:: shell

    python -m randog str

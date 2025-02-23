dice Mode
=========

In dice mode, integer values are generated as total of the dice faces. The format of the command is as follows:

.. code-block:: shell

    randog dice DICE_ROLL [common-options]


Arguments and Options
---------------------

- :code:`DICE_ROLL`:

    - the dice roll value in `dice notation <https://en.wikipedia.org/wiki/Dice_notation>`_ such as :code:`2d6`.

- :code:`common-options`

    - :doc:`common options <doc.as_command.common_option>`


Examples
--------

The simplest example is the following, which outputs the sum of two rolls of 6-sided dice.

.. code-block:: shell

    randog dice 2d6


Repeatedly Generate
~~~~~~~~~~~~~~~~~~~

A single command execution can output results multiple times:

.. code-block:: shell

    # Repeat 10 times
    randog dice 2d6 -r 10

    # Generate list which contains 10 values
    randog dice 2d6 -L 10

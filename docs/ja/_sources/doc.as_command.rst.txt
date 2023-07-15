Run as Command
==============

randog can be used as a command. The basic command format is as follows:

.. code-block:: shell

    python -m randog <MODE> ...

Specify MODE according to the values you want to generate, and specify further arguments to specify more detailed conditions.


Modes
-----

The following modes are available for command execution. Arguments and options available for each mode are described on the detail page for each mode.

.. list-table::
   :header-rows: 1

   * - mode
     - value type
     - command example
     - output example
     - detail

   * - bool
     - :code:`bool`
     - :code:`python -m randog bool`
     - :code:`True`
     - :doc:`detail <doc.as_command.bool>`

   * - int
     - :code:`int`
     - :code:`python -m randog int -100 100`
     - :code:`42`
     -

   * - float
     - :code:`float`
     - :code:`python -m randog float -10 10`
     - :code:`2.826684165562185`
     -

   * - str
     - :code:`str`
     - :code:`python -m randog str`
     - :code:`XTGh3VH1`
     -

   * - decimal
     - :code:`Decimal`
     - :code:`python -m randog decimal -10 10 --decimal-len 2`
     - :code:`3.91`
     -

   * - datetime
     - :code:`datetime`
     - :code:`python -m randog datetime 2022-01-01 2023-01-01`
     - :code:`2022-03-20 12:43:51.110244`
     -

   * - date
     - :code:`date`
     - :code:`python -m randog date 2022-01-01 2023-01-01`
     - :code:`2022-03-20`
     -

   * - time
     - :code:`time`
     - :code:`python -m randog time`
     - :code:`12:43:51.110244`
     -

   * - timedelta
     - :code:`timedelta`
     - :code:`python -m randog timedelta`
     - :code:`17h`
     -

   * - byfile
     - | according to
       | the definition file
     - :code:`python -m randog byfile ./factory_def.py`
     - | according to
       | ./factory_def.py
     - :doc:`detail <doc.as_command.byfile>`


Arguments and Options
---------------------

For mode-specific arguments and options, see the detailed page for each mode.

Several options can be used in any mode; see also:

.. toctree::
   :maxdepth: 2

   doc.as_command.common_option

Details of Modes
----------------

.. toctree::
   :maxdepth: 1

   doc.as_command.bool
   doc.as_command.byfile


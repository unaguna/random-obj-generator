Run as Command
==============

randog can be used as a command. The basic command format is as follows:

.. code-block:: shell

    randog <MODE> ...

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
     - :code:`randog bool`
     - :code:`True`
     - :doc:`detail <doc.as_command.bool>`

   * - int
     - :code:`int`
     - :code:`randog int -100 100`
     - :code:`42`
     - :doc:`detail <doc.as_command.int>`

   * - float
     - :code:`float`
     - :code:`randog float -10 10`
     - :code:`2.826684165562185`
     - :doc:`detail <doc.as_command.float>`

   * - str
     - :code:`str`
     - :code:`randog str`
     - :code:`XTGh3VH1`
     - :doc:`detail <doc.as_command.str>`

   * - decimal
     - :code:`Decimal`
     - :code:`randog decimal -10 10 --decimal-len 2`
     - :code:`3.91`
     - :doc:`detail <doc.as_command.decimal>`

   * - datetime
     - :code:`datetime`
     - :code:`randog datetime 2022-01-01 2023-01-01`
     - :code:`2022-03-20 12:43:51.110244`
     - :doc:`detail <doc.as_command.datetime>`

   * - date
     - :code:`date`
     - :code:`randog date 2022-01-01 2023-01-01`
     - :code:`2022-03-20`
     - :doc:`detail <doc.as_command.date>`

   * - time
     - :code:`time`
     - :code:`randog time`
     - :code:`12:43:51.110244`
     - :doc:`detail <doc.as_command.time>`

   * - timedelta
     - :code:`timedelta`
     - :code:`randog timedelta`
     - :code:`17h`
     - :doc:`detail <doc.as_command.timedelta>`

   * - ipv4
     - :code:`IPv4Address`
     - :code:`randog ipv4`
     - :code:`192.0.2.71`
     - :doc:`detail <doc.as_command.ipv4>`

   * - dice
     - :code:`int`
     - :code:`randog dice 2d6`
     - :code:`9`
     - :doc:`detail <doc.as_command.dice>`

   * - byfile
     - | according to
       | the definition file
     - :code:`randog byfile ./factory_def.py`
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
   doc.as_command.int
   doc.as_command.float
   doc.as_command.str
   doc.as_command.decimal
   doc.as_command.datetime
   doc.as_command.date
   doc.as_command.time
   doc.as_command.timedelta
   doc.as_command.ipv4
   doc.as_command.byfile
   doc.as_command.dice


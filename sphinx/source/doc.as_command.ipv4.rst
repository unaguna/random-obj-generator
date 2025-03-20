ipv4 Mode
=========

In ipv4 mode, IPv4 addresses are generated. The format of the command is as follows:

.. code-block:: shell

    randog ipv4 [NETWORK ...] [--fmt FORMAT] [common-options]

.. warning::
    The option :code:`--fmt` is only available in Python>=3.9.0.


Arguments and Options
---------------------

- :code:`NETWORK` (optional):

    - the space of generated addresses. If multiple addresses are specified, the network will be selected at random each time an address is generated.


- :code:`--fmt FORMAT` (optional):

    - the output format written in `document of IPv4Address.__format__ <https://docs.python.org/3/library/ipaddress.html#ipaddress.IPv4Address.__format__>`_

    .. warning::
        The option :code:`--fmt` is only available in Python>=3.9.0.

- :code:`common-options`

    - :doc:`common options <doc.as_command.common_option>`


Examples
--------

The simplest example is the following:

.. code-block:: shell

    randog ipv4

You can specify the network as follows:

.. code-block:: shell

    # generate an IPv4 address in 203.0.113.1-203.0.113.254
    randog ipv4 203.0.113.0/24

    # generate an IPv4 address in 198.51.100.1-198.51.100.254 or in 203.0.113.1-203.0.113.254
    randog ipv4 198.51.100.0/24 203.0.113.0/24


Format: binary numeral system, etc.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can use the output format written in `document of IPv4Address.__format__ <https://docs.python.org/3/library/ipaddress.html#ipaddress.IPv4Address.__format__>`_ as follows:

.. code-block:: shell

    # output in binary numerical system such as '11000000000000000000001011000100'
    randog ipv4 --fmt b

    # output in hexadecimal such as 'C00002B7'
    randog ipv4 --fmt X

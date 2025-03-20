IPv4 address factory
====================

You can create a factory that generates `IPv4Address <https://docs.python.org/3/library/ipaddress.html#ipaddress.IPv4Address>`_ values with `randipv4 <randog.factory.html#randog.factory.randipv4>`_.

.. note::
    Although a factory of IPv4Address can be created by passing a IPv4Address value as an example to `from_example <randog.factory.html#randog.factory.from_example>`_, it is not possible to specify the creation condition.


Simple factory
--------------

If all that is needed is for the generated value to be an IPv4 address, use `randipv4 <randog.factory.html#randog.factory.randipv4>`_ with no arguments as follows:

.. doctest::

    >>> from ipaddress import IPv4Address
    >>> import randog.factory

    >>> # create a factory
    >>> factory = randog.factory.randipv4()

    >>> generated = factory.next()
    >>> assert isinstance(generated, IPv4Address)


Specify the address space
-------------------------

You can specify the network(s) of generated IPv4 addresses as follows:

.. doctest::

    >>> from ipaddress import IPv4Address, ip_network
    >>> import randog.factory

    >>> # create a factory
    >>> factory1 = randog.factory.randipv4(ip_network("192.168.0.0/24"))
    >>> factory2 = randog.factory.randipv4([ip_network("192.168.0.0/24"), ip_network("192.168.2.0/24")])

    >>> generated1 = factory1.next()
    >>> assert generated1 in ip_network("192.168.0.0/24").hosts()

    >>> generated2 = factory2.next()
    >>> assert generated2 in [*ip_network("192.168.0.0/24").hosts(), *ip_network("192.168.2.0/24").hosts()]

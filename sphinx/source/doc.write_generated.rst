Output Generated Values
=======================

If you want to use the values generated by Factory outside of your program, output them in some way.

The simplest way is to use the print function, as in the following example:

.. doctest::

    >>> import randog.factory

    >>> # factory which generates "a", "b", "c", "d", "e" in order non-randomly
    >>> factory = randog.factory.by_iterator(iter("abcde"))

    >>> for value in factory.iter(5):
    ...     print(value)
    a
    b
    c
    d
    e

In some situations, the following more practical methods may be useful.


As JSON
-------

See :doc:`doc.tips_json`.


As CSV
------

The `generate_to_csv <randog.factory.html#randog.generate_to_csv>`_ function can be used to easily output the generated dictionaries to CSV.


.. note::
    When runs as command, the :code:`--csv` option can be used to produce similar output. See also :ref:`output_as_csv`.

When using generate_to_csv, specify the dictionary's factory, number of rows, output destination, and keys for each column as arguments, as in the following example:

.. doctest::

    >>> import sys
    >>> from itertools import count
    >>> import randog
    >>> import randog.factory

    >>> factory = randog.factory.randdict(
    ...     f1=randog.factory.by_iterator(count(1)),
    ...     f2=randog.factory.by_iterator(iter("abcde")),
    ... )

    >>> randog.generate_to_csv(factory, 5, sys.stdout, csv_columns=["f1", "f2"])
    1,a
    2,b
    3,c
    4,d
    5,e

In addition to column keys, csv_columns can also specify a lambda expression to generate column values, as shown in the following example:

.. code-block:: python

    import randog
    import randog.factory

    factory = randog.factory.randdict(
        name=randog.factory.randstr(length=8),
        created_by=randog.factory.randdate(),
    )
    csv_columns = [
        "name",
        # output with format 'YYYYMMDD'
        lambda d: d["created_by"].strftime("%Y%m%d"),
    ]

    # Example:
    #   sniIz6EK,20240817
    #   QE37X0KD,20241202
    #   smWGOrjO,20241025
    with open("output.csv", mode="w", newline='') as fp:
        randog.generate_to_csv(factory, 3, fp, csv_columns=csv_columns)


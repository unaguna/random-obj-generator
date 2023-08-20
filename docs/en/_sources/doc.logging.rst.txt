Logging
=======

randog logs in `the standard way provided by python <https://docs.python.org/3/library/logging.html>`_. Therefore, you can configure the stream and file output of the logs in the standard way. See also `library docs <https://docs.python.org/3/library/logging.html>`_ or `HOWTO <https://docs.python.org/3/howto/logging.html>`_.

.. note::
    For information on how to output logs when running randog as a command, please read `here <doc.as_command.common_option.html#logging>`_.

.. note::
    randog's log output is not very extensive and may not be very informative. We plan to gradually improve it in the future.

API
---

randog uses the following loggers:

- :code:`randog`: the root of loggers used by randog

    - :code:`randog.cmd`: a logger used by randog command execution

    - :code:`randog.factory`: a logger used in factory generation or other features of factories

    - (increase loggers as appropriate)

.. note::
    When logging randog, it is recommended that a handler be set up for the logger :code:`randog` or the root logger :code:`root`. This is because more loggers may be added in the future, and setting a handler for each child logger may cause unexpected selection and discard.

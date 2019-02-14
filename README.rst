=======
reqlice
=======

Annotate your requirements with the license of each requirement.
Prints the updated requirements file to stdout. Pipe it as you see fit.
Requires Python 3.5 or greater.

------------
Installation
------------

.. code-block:: bash

    pip install -e git+https://github.com/5monkeys/reqlice#egg=reqlice

-----
Usage
-----

To stdout:

.. code-block:: bash

    $ reqlice requirements.txt
    Babel==1.3                        # BSD License  # [license] OSI-Approved: BSD License, BSD
    billiard==3.3.0.20                # BSD License  # [license] OSI-Approved: BSD License, BSD
    celery==3.1.23                    # BSD License  # [license] OSI-Approved: BSD License, BSD

Pipe to file:

.. code-block:: bash

    $ reqlice requirements.txt > updated_requirements.txt

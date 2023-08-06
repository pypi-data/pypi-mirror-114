Installation
============
Navigate to the vspace directory (this directory) and run ``python setup.py``. This command places
some path info in your shell files.

Running VSPACE
--------------
Run ``VSPACE`` on the command line by typing:

.. code-block:: bash

    vspace <input file>

where the input file contains a set of instructions to build the simulations. This
will create a subdirectory containing a) additional subdirectories for each trial,
b) histograms of each varied parameter, and c) a log file containing the value
of each varied parameter in the trial subdirectories.

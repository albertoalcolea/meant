meant
=====

Simple utility to measure the mean time of execution of an app and generate graphs with results.


Dependencies
------------
  * **Python 2**
  * **Matplotlib**


Installation
------------
Place meant.py in `/usr/local/bin`, preferred, or in `/usr/bin` (or any other existing directory in your $PATH environment variable)
Also you can rename it as meant or create an alias in your .bashrc


Usage
-----

    meant [-n repeats] [-u regex] [-g|-gst] [-gname filename] 'app to measure'


### Options
  * `-n` - number of repeats of the test
  * `-u` - you can specify a regex for extracting the execution time to measure (experimental functionality)
  * `-g` - generate a graph with the results of the test
  * `-gst` - generate a graph with the results of the test including the standard desviation
  * `-gname` - name for the graph file (if this parameter is not specified will be created with an automatic name)

### Examples



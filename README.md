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
  * `-n` - number of repeats of the test *(if this parameter is not specified will be executed 20 test)*
  * `-u` - you can specify a regex for extracting the execution time to measure ***(experimental functionality)***
  * `-g` - generate a graph with the results of the test
  * `-gst` - generate a graph with the results of the test including the standard desviation
  * `-gname` - name for the graph file *(if this parameter is not specified will be created with an automatic name)*

### Examples

The basic use

    meant ls

    meant ./tst

    meant "find ~/Documents -name notes"

Test repeated 100 times

    meant -n 100 ./tst

When all test finish will create a file called 'mygraph.png' with a graph of the results

    meant -g -gname mygraph.png ./tst

Same as the previous example but in this case the graph will contain the standard desviation

    menat -gst -gname mygraph.png ./tst

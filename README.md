meant
=====

Simple utility to measure the mean execution time of an app and generate graphs with results.


Dependencies
------------
  * **Python 2**
  * **Matplotlib** *(Only if you want to get graphic results)*


Installation
------------
Place meant.py in `/usr/local/bin`, preferred, or in `/usr/bin` (or any other existing directory in your $PATH environment variable)
Also you can rename it as meant or create an alias in your `.bashrc`. *E.g. `alias meant='python2 ~/scripts/meant.py'`*


Usage
-----

    meant [-h|--help] [-v] [-n repeats] [-f] [-g|-gst [-gname filename]] 'app to measure'


### Options
  * `-h, --help` - Show help
  * `-v` - Verbose mode. Show the execution time for each test
  * `-n` - Number of repeats of the test *(if this parameter is not specified will be executed 20 test)*
  * `-f` - Forces the repetition of the test if the app fails
  * `-g` - Generate a graph with the results of each test
  * `-gst` - Generate a graph with the results of each test including the standard deviation
  * `-gname` - Name for the graph file *(if this parameter is not specified will be created with an automatic name)*

### Examples

The basic use

    meant ls

    meant ./tst

    meant "find ~/Documents -name notes"

Test repeated 100 times

    meant -n 100 ./tst

When all test finish will create a file called 'mygraph.png' with a graph of the results

    meant -g -gname mygraph.png ./tst

Same as the previous example but in this case the graph will contain the standard deviation

    meant -gst -gname mygraph.png ./tst

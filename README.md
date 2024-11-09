[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/kaKQ8FNq)
# Laboratory 3 - Network

## Assignment Deadline: 26/11/2023, 23:59

The aim of these exercises is to build a software abstraction of the
network represented in Fig.[1](#fig:my_label){reference-type="ref"
reference="fig:my_label"} and simulate the signal propagation from an
input node to an output node. In the whole exercise, define the
'constructor', the 'getter' and 'setter' methods for all the class's
attributes, for any class.

![Network sketch.](figures/network.pdf){#fig:my_label
width="0.5\\linewidth"}

# Exercises {#exercises .unnumbered}

1.  Define the class **Signal_information** that has the following
    attributes:

    -   **signal_power**: float

    -   **noise_power**: float

    -   **latency**: float

    -   **path**: list\[string\]

    such that its constructor initializes the signal power to a given
    value, the noise power and the latency to zero and the path as a
    given list of letters that represents the labels of the nodes the
    signal has to travel through. The attribute **latency** is the total
    time delay due to the signal propagation through any network element
    along the path. Define the methods to update the signal and noise
    powers and the latency given an increment of these quantities.
    Define a method to update the path once a node is crossed.

2.  Define the class **Node** that has the following attributes:

    -   **label**: string

    -   **position**: tuple(float, float)

    -   **connected_nodes**: list\[string\]

    -   **successive**: dict\[Line\]

    such that its constructor initializes these values from a python
    dictionary input. The attribute **successive** has to be initialized
    to an empty dictionary. Define a propagate method that update a
    signal_information object modifying its path attribute and call the
    successive element propagate method, accordingly to the specified
    path.

3.  Define the class **Line** that has the following attributes:

    -   **label**: string

    -   **length**: float

    -   **successive**: dict\[Node\]

    The attribute **successive** has to be initialized to an empty dict.
    Define the following methods that update an instance of the
    **signal_information**:

    -   **latency_generation**(): float

    -   **noise_generation**(signal_power): 1e-9 \* signal_power \*
        length

    The light travels through the fiber at around 2/3 of the speed of
    light in the vacuum. Define the line method **latency_generation**
    accordingly. Define a propagate method that updates the signal
    information modifying its noise power and its latency and call the
    successive element propagate method, accordingly to the specified
    path.

4.  Define the class **Network** that has the attributes:

    -   **nodes**: dict\[Node\]

    -   **lines**: dict\[Lines\]

    both the dictionaries have to contain one key for each network
    element that coincide with the element **label**. The value of each
    key has to be an instance of the network element (**Node** or
    **Line**). The constructor of this class has to read the given JSON
    file 'nodes.json', it has to create the instances of all the nodes
    and the lines. The line labels have to be the concatenation of the
    node labels that the line connects (for each couple of connected
    nodes, there would be two lines, one for each direction, e.g. for
    the nodes 'A' and 'B' there would be line 'AB' and 'BA'). The
    lengths of the lines have to be calculated as the minimum distance
    of the connected nodes using their positions. Define the following
    methods:

    -   **connect()**: this function has to set the successive
        attributes of all the network elements as dictionaries (i.e.,
        each node must have a dict of lines and each line must have a
        dictionary of a node);

    -   **find_paths**(string, string): given two node labels, this
        function returns all the paths that connect the two nodes as
        list of node labels. The admissible paths have to cross any node
        at most once;

    -   **propagate**(signal_information): this function has to
        propagate the signal_information through the path specified in
        it and returns the modified spectral_information;

    -   **draw**(): this function has to draw the network using
        matplotlib (nodes as dots and connection as lines).

5.  For all possible paths between all possible node couples, create a
    pandas dataframe that contains the path string as \"A-$>$B-$>$
    \...\", the total accumulated latency, the total accumulated noise
    and the signal to noise ratio obtained with the propagation through
    the paths of a spectral_information with a signal_power of 1 mW.
    Calculate the signal to noise ratio in dB using the formula
    $10 \log(signal\_power/noise\_power)$

    **Additional Notes** All power values have to be considered in
    Watts, all lengths in meters and all latencies in seconds.


    **Additional Notes** All power values have to be considered in
    Watts, all lengths in meters and all latencies in seconds.

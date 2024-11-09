import json
import matplotlib.pyplot as plt
from Lab3.core.math_utils import dist
from Lab3.core.parameters import c


class Signal_information(object):
    def __init__(self):
        self._signal_power = 1e-3
        self._noise_power = 0.0
        self._latency = 0.0
        self._path = []

    @property
    def signal_power(self):
        return self._signal_power

    def update_signal_power(self, incr_p):
        self._signal_power += incr_p
        return self._signal_power

    @property
    def noise_power(self):
        return self._noise_power

    @noise_power.setter
    def noise_power(self, n_pow):
        self._noise_power = n_pow

    def update_noise_power(self, incr_n):
        self._noise_power += incr_n

    @property
    def latency(self):
        return self._latency

    @latency.setter
    def latency(self, lat):
        self.latency = lat

    def update_latency(self, incr_l):
        self._latency += incr_l

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, path):
        self._path = path

    def update_path(self):
        self._path.pop(0)


class Node(object):
    def __init__(self, dict_in):
        self._label = dict_in['label']
        self._position = dict_in['position']
        self._connected_nodes = dict_in['connected_nodes']
        self._successive = {}

    @property
    def label(self):
        return self._label

    @property
    def position(self):
        return self._position

    @property
    def connected_nodes(self):
        return self._connected_nodes

    @property
    def successive(self):
        return self._successive

    @successive.setter
    def successive(self, succ):
        self._successive = succ

    def propagate(self, sig_inf):
        # Remove the first element. The signal has already gone through it
        # Other nodes to travel in the path
        if len(sig_inf.path) > 1:
            sig_inf.update_path()
            currentNodeLabel = self._label
            nextNodeLabel= sig_inf.path[0]

            nextLine = self._successive[currentNodeLabel + nextNodeLabel]
            nextLine.propagate(sig_inf)


class Line(object):
    def __init__(self, label, length):
        self._label = label
        self._length = length
        self._successive = {}  # Label (str) -> Node

    @property
    def label(self):
        return self._label

    @property
    def length(self):
        return self._length

    @property
    def successive(self):
        return self._successive

    @successive.setter
    def successive(self, succ_nd):
        self._successive[succ_nd.label] = succ_nd

    def latency_generation(self):
        return self._length/(2/3*c)

    def noise_generation(self, sig_power):
        return 1e-9*sig_power*self._length

    def propagate(self, signal):
        # AB (line label) -> B
        nextNodeLabel = self.label[1]
        # Take node B
        nextNode = self.successive[nextNodeLabel]
        # Propagate signal through B
        nextNode.propagate(signal)

        latency_increment = self.latency_generation()
        noise_increment = self.noise_generation(signal.signal_power)

        signal.update_latency(latency_increment)
        signal.update_noise_power(noise_increment)


class Network(object):
    def __init__(self, filename):

        self._nodes = {}
        self._lines = {}

        with open(filename) as f:
            # JSON object
            data = json.load(f)
            labels = data.keys()
            for l in labels:
                data[l]["label"] = l
                self._nodes[l] = Node(data[l])
                for n in data[l]['connected_nodes']:
                    line_label = l+n
                    line_len = dist(data[l]['position'], data[n]['position'])
                    self._lines[line_label] = Line(line_label, line_len)

    @property
    def nodes(self):
        return self._nodes

    @property
    def lines(self):
        return self._lines

    def draw(self):
        x = []
        y = []
        for key, value in self._nodes.items():
            for t in value.successive.values():
                for v in t.successive.values():
                    pos_x = v.position[0]
                    pos_y = v.position[1]
                    plt.plot([value.position[0], pos_x], [value.position[1], pos_y], c='black')

            x.append(value.position[0])
            y.append(value.position[1])

        plt.scatter(x, y, s=200, c='red')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title('Network Draw')
        plt.show()

    def find_paths(self, label1, label2):
        crossed = []
        paths = []

        def find_paths_recursive(path, label1, label2):
            crossed.append(label1)

            if label1 == label2:
                paths.append(path.copy())
            else:
                node = self._nodes[label1]
                for el in node.connected_nodes:
                    if el not in crossed:
                        find_paths_recursive(path+[el], el, label2)

            crossed.remove(label1)

        find_paths_recursive([label1], label1, label2)
        return paths

    def connect(self):
        for key, value in self._nodes.items():
            for line in self.lines.keys():
                if line[0] == key:
                    value.successive[line] = self.lines[line]

        for key, value in self._lines.items():
            n1_l = key[1]  # B
            value.successive[n1_l] = self.nodes[n1_l]

    # propagate signal_information through path specified in it
    # and returns the modified spectral information
    def propagate(self, signal_information):
        el = signal_information.path[0]
        node = self._nodes[el]
        node.propagate(signal_information)

    @nodes.setter
    def nodes(self, value):
        self._nodes = value

    @lines.setter
    def lines(self, value):
        self._lines = value

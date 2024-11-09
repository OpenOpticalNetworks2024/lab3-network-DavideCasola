import numpy as np
import pandas as pd
from itertools import permutations
from pathlib import Path
from Lab3.core.elements import *
# Exercise Lab3: Network

root = Path(__file__).parent.parent
input_folder = root/'resources'
file_input = input_folder/'nodes.json'


my_net = Network(file_input)
my_net.connect()
my_net.draw()
column_lab = ['Path', 'Latency[s]', 'Noise Power[W]', 'SNR[dB]']
data = []
mat_data = []

labels = my_net.nodes.keys()
perm = list(permutations(labels, 2))

for el in perm:
    paths = my_net.find_paths(el[0], el[1])
    for path in paths:
        signal = Signal_information()
        signal.path = path.copy()
        my_net.propagate(signal)
        separator = "->"
        path = separator.join(path)
        data.append(path)
        data.append(signal.latency)
        data.append(signal.noise_power)
        data.append(10*np.log10(signal.signal_power/signal.noise_power))
        mat_data += [data]
        data = []

results_frame = pd.DataFrame(mat_data, columns=column_lab)
print(results_frame)
results_frame.to_csv('results.csv', index=False)

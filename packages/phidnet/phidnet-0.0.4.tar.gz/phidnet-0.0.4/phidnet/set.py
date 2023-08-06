import numpy as np
import phidnet.network_data



def weight(axis0, axis1, num):   # Make weights in neural network dictionary
    mat = np.random.randn(axis0, axis1)
    phidnet.network_data.weight[num] = mat
    phidnet.network_data.deltaWeight[num] = None
    return 0



def bias(axis1, num):   # Make biases in neural network dictionary
    mat = np.random.randn(1, axis1)
    phidnet.network_data.bias[num] = mat
    phidnet.network_data.deltaBias[num] = None
    return 0



def build_network(layer_num):   # Build neural network, make nodes and set number of layers
    for i in range(1, layer_num+1):
        phidnet.network_data.a[i] = None

    for i in range(1, layer_num+1):
        phidnet.network_data.z[i] = None

    phidnet.network_data.layerNumber = layer_num
    return 0



def activation_function(activation_f_list):   # Save in list
    phidnet.network_data.active = activation_f_list
    return 0



def input_data(inp):   # Set input data X
    data = np.array(inp)
    phidnet.network_data.X = data
    phidnet.network_data.z[0] = data
    return 0



def target_data(inp):   # Set output data T (Target)
    data = np.array(inp)
    phidnet.network_data.target = data
    return 0
import sys,os,json
import numpy as np

def get_parameters(input):
    with open(input) as data_file:
        source = json.load(data_file)
    return source
        # return dict(
    #     assimilation_rate= source.get('mpi-nodes',1),
    #     cluster_size= source['cluster-size'],
    #     initial_cutoff = source['initial-cutoff']
    # )

def read_parameters(list):
    result = get_parameters(list)
    ETC = result['ETC']
    #for i in list:
        #result.append(get_parameters(i))

    #return result
    return get_parameters(list)

ETC = np.array([
		[1, 2, 3, 4],
		[5, 6, 7, 8],
		[9, 11, 11, 12],
		[9, 13, 11, 12],
		[9, 12, 11, 12]
	])



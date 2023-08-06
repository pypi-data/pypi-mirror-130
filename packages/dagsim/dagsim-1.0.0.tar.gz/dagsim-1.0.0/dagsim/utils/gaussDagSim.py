from dagsim.base import Graph, Generic
import numpy as np 


def func_x2(x0, x1):
	x2 = 2 * x0 + 3 * x1 + np.random.normal(loc=1, scale=0)
	return x2


def func_x3(x0, x2):
	x3 = 1 * x0 + 1 * x2 + np.random.normal(loc=1, scale=0)
	return x3


Node_x0 = Generic(name='x0', function=np.random.normal, arguments={'loc': 1, 'scale': 0})
Node_x1 = Generic(name='x1', function=np.random.normal, arguments={'loc': 1, 'scale': 0})
Node_x2 = Generic(name='x2', function=func_x2, arguments={'x0': Node_x0, 'x1': Node_x1})
Node_x3 = Generic(name='x3', function=func_x3, arguments={'x0': Node_x0, 'x2': Node_x2})

listNodes = [Node_x0, Node_x1, Node_x2, Node_x3]
graph = Graph('myGraph', listNodes)

data = graph.simulate(num_samples=100, csv_name="myFile")

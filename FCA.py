from NNetwork import NNetwork

import math
import multiprocessing
import networkx as nx
import random
import time
import matplotlib.pyplot as plt 

class FCA():
	#colours = array with indices referring to each colour of a node
	def __init__(self, colours, edgelist, vertexlist, kappa):
		self.colours = colours
		self.edgelist = edgelist
		self.vertexlist = vertexlist
		self.net = NNetwork.NNetwork()
		self.kappa = kappa
		self.blinking_colour = math.floor((self.kappa - 1) / 2)
		self.updates = [0] * len(self.vertexlist)

	def add_edges(self):
		return self.net.add_edges(self.edgelist)

	def get_neighbors(self, vertex):
		return self.net.neighbors(vertex)

	# def update(self):
	# 	index = 0
	# 	for update in self.updates:
	# 		if update:
	# 			self.colours[index] += 1
	# 			self.colours[index] %= (self.kappa + 1)
	# 		index += 1
	# 	mark = all(elem == colours[0] for elem in colours)
	# 	if not mark:
	# 		print('Not all colours are equal. Restarting.')
	# 		self.check()

	def check(self):
		count = 1	
		while True:
			for edge in self.edgelist:
				vertex_1 = edge[0]
				vertex_2 = edge[1]
				verticies = [vertex_1, vertex_2]
				neighbors_1 = self.get_neighbors(vertex_1)
				neighbors_2 = self.get_neighbors(vertex_2)
				cond_1 = []
				cond_2 = []
				
				for v in neighbors_1:
					if self.colours[v] == self.blinking_colour:
						cond_1.append(v)

				for v in neighbors_2:
					if self.colours[v] == self.blinking_colour:
						cond_2.append(v)

				if self.colours[verticies[0]] > self.blinking_colour and len(cond_1) >= 1:
					self.updates[verticies[0]] = False
				else:
					self.updates[verticies[0]] = True
				
				if self.colours[verticies[1]] > self.blinking_colour and len(cond_2) >= 1:
					self.updates[verticies[1]] = False
				else:
					self.updates[verticies[1]] = True
			
			index = 0
			for update in self.updates:
				if update:
					self.colours[index] += 1
					self.colours[index] %= (self.kappa + 1)
				index += 1
			
			synch = all(elem == colours[0] for elem in colours)
			if synch:
				break
			else:
				print(str(count) + ': '+ 'Not synchronized yet! Restarting.')
				count += 1



# # #firefly example
# colours = [0, 2]
# edgelist = [[0,1]]
# vertexlist = [0,1]
# kappa = 4



# # random
# colours = [random.randint(0,10) for i in range(20)]
# edgelist = [[random.randint(0, 19), random.randint(0, 19)] for i in range(30)]
# vertexlist = list(range(0,20))
# kappa = 12
# print('colours', colours)
# print('edgelist', edgelist)
# print('vertexlist', vertexlist)

#house example
# colours = [1,2,1,3,4]
# edgelist = [[0,1], [1,2], [2,3], [3,1], [3,4], [4,0]]
# vertexlist = list(range(0,6))
# kappa = 6

#triangle example
# colours = [0, 2, 5, 4]
# edgelist = [[0,1], [0,2], [0,3], [1,0], [1,2], [1,3], [2,0], [2,1], [2,3], [3,0], [3,1], [3,2]]
# vertexlist = [0,1,2,3]
# kappa = 6


#star example
# colours = [0, 1, 2, 3, 4, 5, 3]
# edgelist = [[0,5], [1,5], [2,5], [3,5], [4,5]]
# vertexlist = [0, 1, 2, 3, 4, 5]
# kappa = 6



#square lattice
colours = [4,4,1,2]
edgelist = [[0,1], [1,2], [2,3], [3, 0]]
vertexlist = [0,1,2,3]
kappa = 4

G = nx.Graph()
G.add_edges_from(edgelist)
nx.draw_networkx(G, with_label = True)
plt.savefig('4lattice.png')

graph = FCA(colours, edgelist, vertexlist, kappa)
graph.add_edges()
graph.check()



print(graph.colours)
print('All edges equal!')
from NNetwork import NNetwork

import math
import multiprocessing
import networkx as nx
import random
import time
import matplotlib.pyplot as plt 

class FCA():
	"""Firefly Cellular Automata class made following model proposed in MLOC_writeup question 2.1
	Parameters: -colours: 0 indexed array that contains the colour of each node. Nodes are labeled numerically, starting with 0. 
						 Any ordering for the nodes can be picked, so long as it is consistent in further parameters.
				-edgelist: Array that contains the edges of the graph. Used to generate the graph following documentation in NNetwork package.
				-vertexlist: Array of verticies. However many verticies there are, is what the array should be. Ordering must be consistent with colours array
							 Example: Index 0 of colours should align with index 0 of vertexlist, index 1 of colours with index 1 of vertexlist, etc.
				-kappa: kappa value as chosen in the paper. Can be tuned.	"""
	def __init__(self, colours, edgelist, vertexlist, kappa):
		self.colours = colours
		self.edgelist = edgelist
		self.vertexlist = vertexlist
		self.net = NNetwork.NNetwork()
		self.kappa = kappa
		self.blinking_colour = math.floor((self.kappa - 1) / 2)
		#array telling which indicies of colours are to be updated when checking the update rule
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
		#to check how many steps are being done. More for personal preference.
		count = 1	
		while True:
			#Can see the problem with this, as with larger graphs we are doing unnecessary work. Most likely leading to my abysmal for 20+ vertex, 40+edge graphs.
			for edge in self.edgelist:
				#edge is encoded as (vertex_to, vertex_from) per documentation of NNetwork
				vertex_1 = edge[0]
				vertex_2 = edge[1]
				verticies = [vertex_1, vertex_2]
				#need to assess neighbors for the update rule give by problem 2.1 (1) in MLOC_paper
				neighbors_1 = self.get_neighbors(vertex_1)
				neighbors_2 = self.get_neighbors(vertex_2)
				#arrays to represent the X_t+1 update given in the paper. Used for checking size as the update rule needs it 
				cond_1 = []
				cond_2 = []
				
				#check for size of exact blinking colour nodes per the update rule
				for v in neighbors_1:
					if self.colours[v] == self.blinking_colour:
						cond_1.append(v)
				#check for size of exact blinking colour nodes per the update rule
				for v in neighbors_2:
					if self.colours[v] == self.blinking_colour:
						cond_2.append(v)
				#update rule for vertex 1
				if self.colours[verticies[0]] > self.blinking_colour and len(cond_1) >= 1:
					self.updates[verticies[0]] = False
				else:
					self.updates[verticies[0]] = True
				#update rule for vertex 2
				if self.colours[verticies[1]] > self.blinking_colour and len(cond_2) >= 1:
					self.updates[verticies[1]] = False
				else:
					self.updates[verticies[1]] = True
			
			#updating the colours that satisfied the update rule
			index = 0
			for update in self.updates:
				if update:
					self.colours[index] += 1
					self.colours[index] %= (self.kappa + 1)
				index += 1
			
			#checking to see if all colours of the graph are the same.
			synch = all(elem == colours[0] for elem in colours)
			if synch:
				break
			else:
				print(str(count) + ': '+ 'Not synchronized yet! Restarting.')
				count += 1



"""Various examples as given in the paper where the update rule is mentioned"""


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
# colours = [4,4,1,2]
# edgelist = [[0,1], [1,2], [2,3], [3, 0]]
# vertexlist = [0,1,2,3]
# kappa = 4

#Use of networkX to visualize the graph
G = nx.Graph()
G.add_edges_from(edgelist)
nx.draw_networkx(G, with_label = True)
plt.savefig('4lattice.png')


#main part that runs the FCA
graph = FCA(colours, edgelist, vertexlist, kappa)
graph.add_edges()
graph.check()


#if we make it here, then we have synched and it tells what colour is the final colour
print(graph.colours)
print('All edges equal!')
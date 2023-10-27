import networkx as nx
import pandas as pd
import math
import random

called = 0
position = []
# # graphA = nx.DiGraph()
# graphH = nx.DiGraph()

graphA={}
graphH={}
p = 0.5
c = 0.2
# df=pd.read_csv('../as20000102.csv')
n = 4847571
#n = 229
vertices = list(range(0, n))
vertices = [str(i) for i in vertices]

# graphO=nx.read_gexf('../convertedCitationNetwork.gexf')
# vertices=graphO.nodes

epsilon = 0.1
E1 = set()
Estream = set()
#file = '../as20000102-ver.txt'
file = '../soc-LiveJournal1.txt'
#file='../convertedCitationNetwork.txt'


# file ='../convertedCitationNetwork.txt'
# number of edges in the graph
def edges_to_from(newS, newT, graph, returnList=False):
	global called
	if len(newS) > 1 and len(newT) > 1:
		called += 1
		print("inside E(S,T)-->|S| and |T| : ", len(newS), " ", len(newT))
		print('called: ', called)
	l = []  # [(u, v) for u in newS for v in newT if (u, v) in graph.edges()]
	for node in newT:
		if node in graph.values():
			in_edges=[k for k, v in graph.items() if v == 'y']

			for edge in in_edges:
				if edge in newS:
					l.append((edge,node))
	# l=list(nx.edge_boundary(graph,S,T))
	l = set(l)
	if returnList:
		return l

	return len(l)


def find_duplicates(my_list):
	for edge in my_list:
		if my_list.count(edge) > 1:
			print(edge)
			break
	print('there')


def edges_from_to(newS, newT, graph, returnList=False):
	global called
	newT=set(newT)
	newS=set(newS)

	called+=1
	if len(newS)==1 and len(newT) !=1 :
		print("called from the core loop")

	if len(newS) > 1 and len(newT) > 1:
		#called += 1
		print("inside E(S,T)-->|S| and |T| : ", len(newS), " ", len(newT))
		print('called: ', called)
	l = []  # [(u, v) for u in newS for v in newT if (u, v) in graph.edges()]
	for node in newS:
		
		print('inside node loop: \t', called)
		if node in graph:
			for edge in graph[node]:
				if edge in newT:
					l.append((node,edge))
		# l=list(nx.edge_boundary(graph,S,T))

	#l = set(l)
	if returnList:
		return l

	return len(l)


def add_edge(graphA, line,outGraph=None):
	try:
		v1, v2 = line.strip().split()
	# add the edge to the graph
		if v1 in graphA:
			graphA[v1].add(v2)
		else:
			graphA[v1]=set()
			graphA[v1].add(v2)
		#############add in edges###################
		if outGraph is not None:
			if v2 in outGraph:
				outGraph[v2].add(v1)
			else:
				outGraph[v2]=set()
				outGraph[v2].add(v1)


	except ValueError:
		print('[Error] cant parse line: ', line)

def read_edges(stream, size, graph, outGraph=None):
	print('inside read edges')
	cnt = 0
	size = round(size)

	while True:
		line=stream.readline()
		if not line:
			break
	#for line in stream:
		print(cnt)
		if not line.startswith('#'):
			cnt += 1
			if outGraph is not None:
				add_edge(graph, line,outGraph)
			else:
				add_edge(graph,line,None)
			# if cnt == size:
			# 	position.append(stream.tell())
			# 	break


	graph['size']=cnt

	#position.append(stream.next())
	print('finished reading edges')
	return graph


def read_remaining_edges(stream):
	if position:
		stream.seek(position[0])
		for line in stream:
			try:
				v1, v2 = line.strip().split()
				Estream.add((v1, v2))
			except ValueError:
				print(line)


def create_graphH(stream, E1, s, p, graphH):
	H1 = [edge for edge in E1 if random.random() < p]
	x = random.binomial(s, p)
	read_edges(stream, x, graphH)
	graphH = create_graph_with_edges(graphH, H1)
	return graphH


def density(S, T, graph):
	return edges_from_to(S, T, graph) / (math.sqrt(len(S) * len(T)))


def create_graph_with_edges(completeG, edges):
	edge_dict={}
	cnt=0
	for edge in edges:
		cnt+=1
		v1,v2=edge[0],edge[1]
		if v1 in edge_dict:
			edge_dict[v1].add(v2)
		else:
			edge_dict[v1]=set()
			edge_dict[v1].add(v2)

	edge_dict['size']=cnt
	return edge_dict


def bahmaniAlgorithm(filePath, c):
	entireGraph = {}
	outGraph={}
	with open(filePath, 'r') as stream:
		read_edges(stream, 5000000, entireGraph,outGraph)

	# entireGraph=nx.read_gexf(filePath)
	S,T=set(vertices),set(vertices)
	#S, T = entireGraph.nodes, entireGraph.nodes
	S1, T1 = S, T
	maxD = 0
	iterNumber = 0

	while S and T:
		iterNumber += 1
		metric = (1 + epsilon) * edges_from_to(S, T, entireGraph)
		print('***********************metric computed***************************')
		if len(S) / len(T) >= c:
			A = [node for node in S if edges_from_to([node], T, entireGraph) <= metric / len(S)]
			S = S - set(A)
			print("Size of S:",len(S))
		else:
			B = [node for node in T if edges_from_to([node], S, outGraph) <= metric / len(T)]
			T = T - set(B)
			print("Size of T:",len(T))

		if len(S) == 0 or len(T) == 0:
			break
		else:
			if density(S, T, entireGraph) > density(S1, T1, entireGraph):
				maxD = density(S, T, entireGraph)
				S1 = S
				T1 = T
	print('Their iterations: \t', iterNumber)
	print(maxD)
	return maxD


def algorithm1(edges, c):
	# construct temp graph
	# S, T = set(vertices), set(vertices)
	completeG = nx.DiGraph()
	completeG = create_graph_with_edges(completeG, edges)
	S,T=set(completeG.keys()),set(completeG.keys())
	S.remove('size')
	T.remove('size')
	S1, T1 = S, T
	maxD = 0
	innerIter = 0

	while S and T:
		print("|S| and |T| : ", len(S), " ", len(T))
		innerIter += 1
		prob = (96 * n * math.log10(n)) / (pow(epsilon, 2) * edges_from_to(S, T, completeG) * (1 - epsilon))
		prob = min(prob, 1)

		#tempG = nx.DiGraph()
		tempG={}
		edgesFromStoT = edges_from_to(S, T, completeG, returnList=True)
		for edge in edgesFromStoT:
			if random.random() < prob:
				v1,v2=edge
				if v1 in tempG:
					tempG[v1].add(v2)
				else:
					tempG[v1]=set()
					tempG[v1].add(v2)

		metric = (edges_from_to(S, T, tempG)) * (1 + epsilon)
		cnt=0
		if len(S) / len(T) >= c:
			A=set()
			for node in S:
				cnt+=1
				print("node:",cnt)
				if edges_from_to([node],T,tempG) <= metric/len(S):
					A.add(node)

		#	A = [node for node in S if edges_from_to([node], T, tempG) <= metric / len(S)]
			S = S - set(A)
		else:
			B = [node for node in T if edges_from_to(S, [node], tempG) <= metric / len(T)]
			T = T - set(B)

		if len(S) == 0 or len(T) == 0:
			break
		else:
			d = density(S, T, completeG)
			print("*************************************density***************************************:\t", d)
			if density(S, T, completeG) > density(S1, T1, completeG):
				S1 = S
				T1 = T
				maxD = density(S, T, completeG)
		# if d > maxD:
		# 	maxD=d
		# 	S1=S
		# 	T1=T

	print(len(S1))
	print(len(T1))
	print("Our Density:\t", maxD)
	print("\n Inner iteration: \t ", innerIter)
	return maxD

def setOfEdges(graph):
	edgeSet=[]
	for node1 in graph:
		if node1 != 'size':
			for node2 in graph[node1]:
				edgeSet.append((node1,node2))

	return edgeSet

S, T = vertices, vertices
S1, T1 = S, T
c = 1 / n
dmax = 0
cmax = c
c=0.8
d = bahmaniAlgorithm(file, c)
print("*************************density*****************************",d)

# while c <= n:
# 	c = c * (1 + epsilon)
# 	d = bahmaniAlgorithm('../as20000102-ver.txt', c)
# 	if d > dmax:
# 		dmax = d
# 		cmax = c
# print("***********************max density for respective c***************************************:\t", dmax, "======",
# 	  cmax)
exit()

while True:
	s = 13233
	# s=1468364884
	s1 = 0
	# set of next edges
	nextEdges = (96 * n * math.log10(n))  # /pow(epsilon,2)
	with open(file, 'r') as stream:
		graphA=read_edges(stream, nextEdges, graphA)

	# graphA is read
	edgesBetween = edges_from_to(S, T, graphA)
	if edgesBetween >= (192 * math.log10(n)) / pow(epsilon, 2) and graphA['size'] == nextEdges:
		s1 = (s * (1 - epsilon) * edgesBetween) / graphA['size'] + len(E1)

	else:
		with open(file, 'r') as stream:
			read_remaining_edges(stream)
		E1 = E1.union(set(setOfEdges(graphA))).union(Estream)
		c = 1 / n
		dmax = 0
		cmax =  0.02033110732313870885
		# while c <= n:
		# 	c = c * (1 + epsilon)
		# 	d = algorithm1(E1, c)
		# 	if d > dmax:
		# 		dmax = d
		# 		cmax = c

		d=algorithm1(E1,cmax)
		print("***********************max density for respective c***************************************:\t", dmax,
			  "======", cmax)

		break

	E1 = E1.union(set(graphA.edges))
	# haven't added all the nodes
	prob = (96 * n * math.log10(n)) / (pow(epsilon, 2) * s1 * (1 - epsilon))
	p = min(prob, 1)
	graphH = create_graphH(stream, E1, s1 - len(E1), p, graphH)
	c = 0.2
	metric = (1 + epsilon) * len(graphH.edges)
	if len(S) / len(T) >= c:
		A = [node for node in S if edges_from_to(node, T) <= metric / len(S)]
		S = S - A
	else:
		B = [node for node in T if edges_from_to(S, node) <= metric / len(T)]
		T = T - B

	if density(S, T) > density(S1, T1):
		S1 = S
		T1 = T

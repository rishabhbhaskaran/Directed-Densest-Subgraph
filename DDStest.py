import networkx as nx
import pandas as pd
import math
import random

position=[]
graphA=nx.DiGraph()
graphH=nx.DiGraph()
p=0.5
c=0.5
# df=pd.read_csv('../twitter-2010-ids.csv')
# vertices=df['node_id']

graphO=nx.read_gexf('../convertedCitationNetwork.gexf')
vertices=graphO.nodes

n=229 #41652230
epsilon=0.1
E1=set()
Estream=set()
#file='../twitter-2010.txt'
file ='../convertedCitationNetwork.txt'
 #number of edges in the graph

def edges_from_to(newS,newT,graph,returnList=False):
	l= []#[(u, v) for u in newS for v in newT if (u, v) in graph.edges()]
	for node in newS:
		for edge in graph.out_edges(node):
			if edge[1] in newT:
				l.append(edge)
	#l=list(nx.edge_boundary(graph,S,T))
	if returnList:
		return l

	return len(l)

def add_edge(graphA,line):
	v1, v2 = line.strip().split()
	# add the edge to the graph
	graphA.add_edge(v1, v2)


def read_edges(stream,size,graph):
	print('inside read edges')
	cnt = 0
	size=round(size)
	for line in stream:
		cnt += 1
		add_edge(graph,line)
		if cnt == size:
			break
	position.append(stream.tell())
	print('finished reading edges')

def read_remaining_edges(stream):
	stream.seek(position[0])
	for line in stream:
		v1, v2 = line.strip().split()
		Estream.add([v1,v2])

def create_graphH(stream, E1, s, p,graphH):
	H1=[edge for edge in E1 if random.random() < p]
	x=random.binomial(s,p)
	read_edges(stream,x,graphH)
	graphH=create_graph_with_edges(graphH,H1)
	return graphH




def density(S,T,graph):
	return edges_from_to(S,T,graph)/(math.sqrt(len(S)*len(T)))

def create_graph_with_edges(completeG,edges):
	for edge in edges:
		completeG.add_edge(edge[0],edge[1])
	return completeG


def bahmaniAlgorithm(filePath):
	entireGraph=nx.read_gexf(filePath)
	c=0.5
	S,T=entireGraph.nodes,entireGraph.nodes
	S1,T1=S,T
	maxD=0
	iterNumber=0


	while S and T:
		iterNumber+=1
		metric = (1+epsilon) * edges_from_to(S,T,entireGraph)
		if len(S)/len(T) >= c:
			A = [node for node in S if edges_from_to([node], T, entireGraph) <= metric / len(S)]
			S=S-set(A)
		else:
			B = [node for node in T if edges_from_to(S,[node], entireGraph) <= metric / len(T)]
			T=T-set(B)

		if len(S)==0 or len(T)==0:
			break
		else:
			if density(S, T, entireGraph) > density(S1, T1, entireGraph):
				maxD=density(S, T, entireGraph)
				S1=S
				T1=T
	print('Their iterations: \t',iterNumber)
	print(maxD)

def algorithm1(edges):
	#construct temp graph
	innerIter=0
	S,T=vertices,vertices
	S1,T1=S,T
	completeG=nx.DiGraph()
	prob = (96 * n * math.log10(n)) / (pow(epsilon, 2) * edges_from_to(S,T,graphO) * (1 - epsilon))
	prob = min(prob, 1)
	completeG=create_graph_with_edges(completeG,edges)
	while S and T:
		innerIter+=1
		tempG=nx.DiGraph()
		for edge in edges_from_to(S,T,completeG,returnList=True):
			if random.random() < prob:
				tempG.add_edge(edge[0],edge[1])

		metric = len(tempG.edges) * (1 + epsilon)
		if len(S)/len(T) >=c:
			A=[node for node in S if edges_from_to([node],T,tempG) <= metric/len(S)]
			S=S-set(A)
		else:
			B=[node for node in T if edges_from_to(S,[node],tempG) <= metric/len(T)]
			T=T-set(B)


		if len(S)==0 or len(T)==0:
			break
		else:
			if density(S, T, completeG) > density(S1, T1, completeG):
				S1=S
				T1=T
	print(len(S1))
	print(len(T1))
	print("Our Density:\t",density(S1,T1,completeG))
	print("\n Inner iteration: \t ",innerIter)


S,T= vertices,vertices
S1,T1=S,T
numberOuter=0

bahmaniAlgorithm('../convertedCitationNetwork.gexf')
exit()

while True:
	numberOuter+=1
	s = 5856
	#s=1468364884
	s1=0
	#set of next edges
	nextEdges= (96*n*math.log10(n))/pow(epsilon,2)
	with open(file,'r') as stream:
		read_edges(stream,nextEdges,graphA)

	#graphA is read
	edgesBetween= edges_from_to(S,T,graphA)
	if edgesBetween >= (192*math.log10(n))/pow(epsilon,2) and graphA.number_of_edges()==nextEdges:
		s1= (s*(1- epsilon)*edgesBetween)/graphA.number_of_edges() + len(E1)
	else:
		with open(file, 'r') as stream:
			read_remaining_edges(stream)
		E1= E1.union(set(graphA.edges())).union(Estream)
		algorithm1(E1)
		print("Outer loop number for our algo: \t",numberOuter)
		break

	E1=E1.union(set(graphA.edges))
	#haven't added all the nodes
	prob=(96*n*math.log10(n))/(pow(epsilon,2)*s1*(1-epsilon))
	p= min(prob,1)
	graphH=create_graphH(stream, E1, s1 - len(E1), p, graphH)
	c=0.2
	metric= (1 + epsilon) * len(graphH.edges)
	if len(S)/len(T) >= c:
		A=[node for node in S if edges_from_to(node,T) <= metric/len(S)]
		S=S-A
	else:
		B = [node for node in T if edges_from_to(S,node) <= metric/len(T)]
		T=T-B

	if density(S,T) > density(S1,T1):
		S1=S
		T1=T













edge_dict={}
count=0
with open('../twitter-2010.txt') as stream:
    for line in stream:
        v1, v2 = line.strip().split()
        print(v1,v2)
        count+=1
        print(count)
        # add the edge to the graph
        if v1 in edge_dict:
            edge_dict[v1].append(v2)
        else:
            edge_dict[v1]=[v2]

print(edge_dict.__sizeof__()/1024/1024)
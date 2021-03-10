import networkx as nx

def cc_dot(nu,nv):
    return float(len(nu & nv))/len(nu | nv)

def cc_max(nu,nv):
    return float(len(nu & nv))/max(len(nu),len(nv))

def cc_min(nu,nv):
    return float(len(nu & nv))/min(len(nu),len(nv))

modes={'dot':cc_dot,
       'min':cc_min,
       'max':cc_max}

def clustering(G, nodes=None, mode='dot'):
    print("clustering")
    if not nx.algorithms.bipartite.is_bipartite(G):
        raise nx.NetworkXError("Graph is not bipartite")
    try:
        cc_func = modes[mode]
    except KeyError:
        raise nx.NetworkXError("Mode for bipartite clustering must be: dot, min or max")
    nodes = G
    ccs = {}
    for v in nodes:
        cc = 0.0
        #print(G[v])
        nbrs2 = set([u for nbr in G[v] for u in G[nbr]]) - set([v])
        #print(nbrs2)
        for u in nbrs2:
            cc += cc_func(set(G[u]), set(G[v]))
        if cc > 0.0:  # len(nbrs2)>0
            cc /= len(nbrs2)
        ccs[v] = cc
    print(type(ccs))
    print(ccs)
    return ccs
def average_clustering(G, nodes=None, mode='dot'):
    print("average clustering")
    if nodes is None:
        nodes=G
    ccs=clustering(G, nodes=nodes, mode=mode)
    print(ccs)
    res=float(sum(ccs[v] for v in nodes))/len(nodes)
    print(type(res))
    print(res)
def main():
    inpath = "/home/zc/IDBdata/three-non5-22/ex23/mid-train/spe_comp_wei_spark.txt/part-00000"
    infile = open(inpath)
    G = nx.Graph()
    for line in infile:
        line = line.strip()
        lst = line.split('\t')
        G.add_edge(lst[0], lst[1], weight=lst[2])
    infile.close()
    print(G.nodes())
    print(G.edges())
    print(G.number_of_edges())
    #clustering(G,None,'dot')
    average_clustering(G,None,'dot')
main()
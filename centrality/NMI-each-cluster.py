import sys, os, gzip
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def get_annotated_key(keyinfo):
    '''
    Label each read with annotated transcript id
    If not labelled, use "na"
    return a dictionary seqID -> transcript_id
    '''
    ## read annotated transcripts
    print("Number of reads in the annotation: " + '{:,d}'.format(len(keyinfo.keys())))
    known_clusters = pd.DataFrame.from_dict(keyinfo, 'index')
    known_clusters = known_clusters.rename(columns={0: 'transcript'})
    known_counts = known_clusters.groupby(['transcript']).size()
    print("Total reads in annotated clusters: " + '{:,d}'.format(known_counts[known_counts > 1].sum()))
    print("Total annotated clusters: " + '{:,d}'.format(sum(known_counts > 1)))
    print("The top 10 biggest annotated clusters are:")
    print(known_counts.sort_values(ascending=False)[0:10])
    return keyinfo

def annotate_clusters(cluster, annotations):
    '''
    parse spark cluster results
    cluster file format is: seqid \t cluster_id
    return: [seq_name, cluster_id, annotation_transcript]
    '''
    results = []
    total_clustered_reads = 0
    total_clustered_annotated = 0
    for lines in cluster:  # .readlines():
        seq_id, group_id = lines.strip("\n").split("\t")
        total_clustered_reads += 1
        try:
            if int(group_id) > 0 and annotations[seq_id] != 'na':
                results.append([seq_id, group_id, annotations[seq_id]])
                total_clustered_annotated += 1
        except:
            continue
    print( "Total reads in clusters: " + '{:,d}'.format(total_clustered_reads))
    print("Total annotated reads in clusters: " + '{:,d}'.format(total_clustered_annotated))
    return pd.DataFrame(results)

def get_nmi(config):
    cluster_ids = set(config[1])
    data = []
    for name,group in config.groupby([2]):
        d = {c:0 for c in cluster_ids}
        for g in group[1]:
            d[g] +=1
        d.pop('-1', None) # remove unclustered reads
        data.append([d[k] for k in sorted(d.keys())])
    data = np.array(data).astype(float)
    tc = np.copy(data)
    tcp = tc/np.sum(tc)
    ws = [ np.sum(tc[i])/(np.sum(tc)+0.0000000000001) for i in range(len(tc))]
    cs = [ np.sum(np.transpose(tc)[i])/(np.sum(tc)+0.0000000000001) for i in range(len(np.transpose(tc)))]
    print(ws,cs)
    if len(ws)>0 and len(cs)>0:
        II = 0
        for i in range(len(ws)):
            for j in range(len(cs)):
                II += tcp[i][j] * np.log((tcp[i][j])/(cs[j]*ws[i]+0.0000000000001) + 0.000000000001)
        Hc = np.sum([ -csi * np.log(csi + 0.000000000001) for csi in cs])
        Hw = np.sum([ -cwi * np.log(cwi + 0.000000000001) for cwi in ws])
        H = (Hc+Hw)*0.5
        NMI = II/H
        return NMI,II
    else:
        return 'len 1',"err"

def main():
    keyfile = {"A":1,"B":1,"C":1,"D":1,"E":1,"F":1}
    #{"A":1,"B":1,"C":1,"D":1,"E":1,"F":1,"G":2,"H":2,"I":2,"J":2,"K":2,"L":2,"M":3,"N":3,"O":3,"P":3,"Q":3}
    keyinfo = get_annotated_key(keyfile)
    #print(keyinfo)
    l=["A	1","B	2","C	1","D	1","E	1","F	1","G	1","H	2","I	2",
       "J	2","K	2","L	3","M	1","N	1","O	3","P	3","Q	3"]
    l2=["A	4","B	5","C	6","D	7","E	8","F	9","G	10","H	11","I	12",
       "J	13","K	14","L	15","M	16","N	20","O	20","P	20","Q	20"]
    l3=["A	1","B	1","C	1","D	1","E	1","F	1","G	2","H	2","I	2",
       "J	2","K	2","L	2","M	4","N	4","O	4","P	5","Q	5"]
    l4 = ["A	4", "B	4", "C	4", "D	4", "E	4", "F	4", "G	5", "H	5", "I	5",
          "J	5", "K	5", "L	5", "M	6", "N	6", "O	6", "P	6", "Q	6"]
    l5=["A	4", "K	4", "B	4", "M	4","E	4", "F	4","O	4", "P	4", "Q	4"]
    config1 = annotate_clusters(l5, keyinfo)
    print(config1)
    nmi, ii = get_nmi(config1)
    print(nmi)
main()
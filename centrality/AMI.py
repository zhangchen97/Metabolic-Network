import sys, os, gzip
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def get_annotated_key(keyfile):
    '''
    Label each read with annotated transcript id
    If not labelled, use "na"
    return a dictionary seqID -> transcript_id
    '''
    ## read annotated transcripts
    keyinfo = {}
    if not (os.path.exists(keyfile)):
        print("at least one of the input files are not found.")
        sys.exit(0)
    with open(keyfile, 'r') as KEY:
        for lines in KEY:  # .readlines():
            try:
                anarray = lines.strip("\n").split("\t")
                keyinfo[anarray[0]] = anarray[1]  # there was an extra >
            except:
                continue
    KEY.close()
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
    if not os.path.exists(cluster):
        print("Cluster file not found.")
        sys.exit(0)

    results = []
    total_clustered_reads = 0
    total_clustered_annotated = 0
    with open(cluster, 'r') as IN:
        for lines in IN:  # .readlines():
            seq_id, group_id = lines.strip("\n").split("\t")
            total_clustered_reads += 1
            try:
                if int(group_id) > 0 and annotations[seq_id] != 'na':
                    results.append([seq_id, group_id, annotations[seq_id]])
                    total_clustered_annotated += 1
            except:
                continue
    IN.close()
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
    if len(ws)>1 and len(cs)>1:
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
        return 'len 1'

def main():
    keyfile = "/home/zc/IDBdata/IBD-non-species-compound-static/non/module_non_ex12_train_nmi.txt"
    keyinfo = get_annotated_key(keyfile)
    #print(keyinfo)
    config1 = annotate_clusters('/home/zc/IDBdata/IBD-non-species-compound-static/ibd/module_ibd_ex12_train_nmi.txt', keyinfo)
    nmi, ii = get_nmi(config1)
    print(nmi)
main()
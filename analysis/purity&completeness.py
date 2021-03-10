import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()
plt.rcParams['figure.figsize'] = (12, 8)

def read_gt(fpath):
    gt = pd.read_csv(fpath, header=None, sep="\t")
    gt.columns = ['node', 'cluster']
    print(gt.head())
    print("num:")
    print(gt.node.value_counts().value_counts())
    return gt


def read_cluster(fpath):
    clusters = pd.read_csv(fpath, header=None, sep="\t")
    clusters.columns = ['node', 'cluster']
    print(clusters.head())
    return clusters


def analysize(label, clusters):
    ##聚类结果
    ret = {}
    ret["Total #reads"] = len(clusters['cluster'])
    ret["clusteing #clusters"] = len(set(clusters['cluster']))
    ret['ground_truth #clusters'] = len(set(label['cluster']))
    # plt.hist(np.log10(clusters.cluster.value_counts()),bins=50);plt.title("historgram of cluster size (log10 scale)");plt.show()
    print("ret: ")
    print(ret)
    df = pd.merge(clusters, label, on=['node'])
    df.columns = ['qname', 'cid', 'rname']
    print(df)
    ret["Filtered #clusters"] = len(set(df['cid']))
    ret["Filtered #reads"] = len(df['cid'])
    ret["Filtered #ground_truth"] = len(set(df['rname']))
    # plt.hist(np.log10(df['cid'].value_counts()),bins=50);plt.title("historgram of cluster size (log10 scale)");plt.show()
    ret['mean cluster size:'] = df['cid'].value_counts().mean()
    ret['median cluster size:'] = df['cid'].value_counts().median()
    # ret["nmi"]=nmi(df.rname.values, df.cid.values)
    # print df.shape,gt.shape,clusters.shape, list(df.columns)
    #断言,在表达式为 false 的时候触发异常
    assert len(df) > 0
    df20 = df.groupby(['cid', 'rname'])['qname'].count()
    df2 = df20.reset_index(name="count")
    print("df2")
    print(df2)
    ##clustering cluster condition
    df30 = df[['cid', 'qname']].groupby('cid')['qname'].count()
    df3 = df30.reset_index(name='c_count')
    print("df3")
    print(df3)
    ##label cluster condition
    df4 = df[['rname', 'qname']].groupby('rname')['qname'].count().reset_index(name='r_count')
    print("df4")
    print(df4)
    newdf = pd.merge(pd.merge(df2, df3, on='cid', how='left'), df4, on='rname', how='left')
    print("newdf")
    print(newdf)
    newdf = newdf[newdf['c_count'] > 1]
    newdf['purification'] = newdf['count'] / newdf['c_count']
    newdf['completeness'] = newdf['count'] / newdf['r_count']
    stats1 = newdf.groupby(['cid'])[['purification']].max().reset_index()
    stats1['c_count'] = stats1['cid'].map(df30.to_dict())
    # stats1['purification'].hist(bins=50);plt.title("historgram of purification");plt.show()
    stats1['pw_count'] = stats1['purification'] * stats1['c_count']
    print("stats1")
    print(stats1)
    #np.log10(stats1['pw_count']).hist(bins=50);plt.title("historgram of purification weighted cluster size");plt.show()
    stats2 = newdf.groupby(['rname'])[['completeness']].max().reset_index()
    # (stats2['completeness']).hist(bins=50);plt.title("historgram of completeness");plt.show()
    ret["%100 purification:"] = (stats1['purification'] == 1).mean()
    ret[">%95 purification:"] = (stats1['purification'] >= 0.95).mean()
    ret["mean purification:"] = stats1['purification'].mean()
    ret["median purification:"] = stats1['purification'].median()
    ret["%100 completeness:"] = (stats2['completeness'] == 1).mean()
    ret[">%80 completeness:"] = (stats2['completeness'] >= 0.80).mean()
    ret["mean completeness:"] = stats2['completeness'].mean()
    ret["median completeness:"] = stats2['completeness'].median()
    print("ret res: ")
    print(ret)
    return ret, newdf
def main():
    label=read_gt("/home/zc/IDBdata/three-non5/purity&comple/module_non_ex23_train_valicommon.txt")
    clusters=read_cluster("/home/zc/IDBdata/three-non5/purity&comple/module_ibd_ex23_train_valicommon.txt")
    ret, df = analysize(label, clusters)
    df_local_purity = df.groupby(['cid'])[['c_count', 'purification']].max().reset_index().sort_values('c_count', ascending=False)
    df_local_completeness = df.groupby(['rname'])[['r_count', 'completeness']].max().reset_index().sort_values(
        'r_count', ascending=False)

    merge = [df_local_completeness['completeness'] * 100, df_local_purity['purification'] * 100]
    localcolor = 'darkgray'
    plt.subplots_adjust(wspace=.1, hspace=.1)
    ax1 = plt.subplot(1, 1,1)
    medianprops = dict(linestyle='-', linewidth=4, color='black')
    ##violin graph
    sns.violinplot(data=merge, width=0.5, inner=None, color="w", scale='width')

    bplot = plt.boxplot(merge, showfliers=False, positions=[0, 1], patch_artist=True, widths=0.10,
                    medianprops=medianprops)
    ax1.set_xlabel("cluster purity and completeness distribution", fontsize=16)
    colors = [localcolor,localcolor, localcolor]  # 颜色填充
    for patch, color in zip(bplot['boxes'], colors): patch.set_facecolor(color)
    ax1.tick_params(labelsize=10)
    plt.setp(ax1, xticks=[0.0, 1.0], xticklabels=['completeness', 'purity'])
    ax1.legend([bplot["boxes"][0], bplot["boxes"][1]],[],bbox_to_anchor=(0.5, 0.7),fontsize=10)  # 图例
    plt.tight_layout()
    plt.show()
main()
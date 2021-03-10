from collections import Counter
##研究health样本和IBD样本内的物种：（common,health only,IBD only）
#日后还要分析他们分别在多少个样本内出现以及abundance。
from matplotlib_venn import venn2
from matplotlib import pyplot as plt
health_path="/home/zc/IDBdata/all_data/species-analysis/allnon_specie_abudance_ave.csv"
ibd_path="/home/zc/IDBdata/all_data/species-analysis/allibd_specie_abudance_ave.csv"

health_spe_set=set()
ibd_spe_set=set()
# read health file
health_file=open(health_path,'r')
for line in health_file:
    line=line.strip()
    l1=line.split('\t')
    health_spe_set.add(l1[0])
health_file.close()

# read IBD file.
ibd_file=open(ibd_path,'r')
for line in ibd_file:
    line=line.strip()
    l1=line.split('\t')
    ibd_spe_set.add(l1[0])

ibd_file.close()
## analysis the both.
##species交集
spe_intersection_set=ibd_spe_set.intersection(health_spe_set)
##species差集
health_spe_diff=health_spe_set.difference(ibd_spe_set)
ibd_spe_diff=ibd_spe_set.difference(health_spe_set)
#species并集
spe_union_set=ibd_spe_set.union(health_spe_set)
print("species----------------- species -------------------------species")
print("spe_intersection:"+str(len(spe_intersection_set)))
print("health_spe_diff:"+str(len(health_spe_diff)))
print("ibd_spe_diff:"+str(len(ibd_spe_diff)))
print("spe_union_set:"+str(len(spe_union_set)))
out=venn2(subsets=[set(health_spe_set),set(ibd_spe_set)],
      set_labels=("health","ibd"),set_colors=('r','g'))
plt.title("Microbes with abundance greater than 1%",fontsize=16)
plt.show()

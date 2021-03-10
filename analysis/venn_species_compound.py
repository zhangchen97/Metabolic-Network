from collections import Counter
##研究health样本和IBD样本内的物种：（common,health only,IBD only）
#日后还要分析他们分别在多少个样本内出现以及abundance。

health_path="/home/zc/IDBdata/IBD-non-species-compound-static/non/spe_comp_wei_spark.txt/part-00000"
ibd_path="/home/zc/IDBdata/IBD-non-species-compound-static/ibd/spe_comp_wei_spark.txt/part-00000"

health_spe_set=set()
health_com_set=set()

ibd_spe_set=set()
ibd_com_set=set()

# read health file
health_file=open(health_path,'r')
for line in health_file:
    line=line.strip()
    l1=line.split('\t')
    health_spe_set.add(l1[0])
    health_com_set.add(l1[1])
health_file.close()

# read IBD file.
ibd_file=open(ibd_path,'r')
for line in ibd_file:
    line=line.strip()
    l1=line.split('\t')
    ibd_spe_set.add(l1[0])
    ibd_com_set.add(l1[1])
ibd_file.close()

## analysis the both.
###########################################Species###############################################
# species交集
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

print("--------------------")
####################################################Compound##################################################
##compound交集
com_intersection_set=health_com_set.intersection(ibd_com_set)
##compound差集
health_com_diff=health_com_set.difference(ibd_com_set)
ibd_com_diff=ibd_com_set.difference(health_com_set)
#compound并集
com_union_set=health_com_set.union(ibd_com_set)
print("compound-------------------- compound -----------------------------compound")
print("com_intersection_set:"+str(len(com_intersection_set)))
print("health_com_diff:"+str(len(health_com_diff)))
print("ibd_com_diff:"+str(len(ibd_com_diff)))
print("com_union_set:"+str(len(com_union_set)))


from matplotlib_venn import venn2
from matplotlib import pyplot as plt
#species
out=venn2(subsets=[set(health_spe_set),set(ibd_spe_set)],
      set_labels=("health","ibd"),set_colors=('r','g'))
plt.title("Microbes",fontsize=16)
plt.show()
###compound
out2=venn2(subsets=[set(health_com_set),set(ibd_com_set)],
      set_labels=("health","ibd"),set_colors=('r','g'))
plt.title("Compounds",fontsize=16)
plt.show()
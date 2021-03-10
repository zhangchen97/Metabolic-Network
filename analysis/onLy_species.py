from collections import Counter
##研究health样本和IBD样本内的物种：（common,health only,IBD only）
#日后还要分析他们分别在多少个样本内出现以及abundance。

health_path="/home/zc/IDBdata/all_data/species-analysis/non-species-common0.1-ave.csv"
ibd_path="/home/zc/IDBdata/all_data/species-analysis/ibd-species-common0.1-ave.csv"

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
species_list=[ "Clostridium_hathewayi", "Clostridium_bolteae",
    "Escherichia_coli","Eubacterium_rectale","Faecalibacterium_prausnitzii","Haemophilus_parainfluenzae",
    "Klebsiella_pneumoniae","Roseburia_hominis", "Ruminococcus_torques", "Ruminococcus_gnavus",
    "Bacteroides_fragilis","Bifidobacterium_adolescentis","Clostridium_leptum","Dialister_invisus","Prevotella_copri"]
print("no list common")
no_list_common=[]
for specie in species_list:
    if specie not in spe_intersection_set:
        no_list_common.append(specie)
print(len(no_list_common))
print(no_list_common)
print("no list ibd")

no_list_ibd=[]
for specie in species_list:
    if specie not in ibd_spe_set:
        no_list_ibd.append(specie)
print(len(no_list_ibd))
print(no_list_ibd)

print("no list nonibd")
no_list_nonibd=[]
for specie in species_list:
    if specie not in health_spe_set:
        no_list_nonibd.append(specie)
print(no_list_nonibd)
print(len(no_list_nonibd))

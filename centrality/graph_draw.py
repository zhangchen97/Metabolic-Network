from collections import Counter
##研究health样本和IBD样本内的物种：（common,health only,IBD only）
#日后还要分析他们分别在多少个样本内出现以及abundance。

health_path="/home/zc/IDBdata/three-non5-22/ex12/mid-train/spece_compound_weight.txt"
ibd_path="/home/zc/IDBdata/three-IBD5/ex12/mid-train/spece_compound_weight.txt"

health_spe_set=set()
health_com_set=set()

ibd_spe_set=set()
ibd_com_set=set()

# read health file
health_file=open(health_path,'r')
for line in health_file:
    line=line.strip()
    l1=line.split('\t')
    health_com_set.add(l1[1])
    health_spe_set.add(l1[0])
health_file.close()

# read IBD file.
ibd_file=open(ibd_path,'r')
for line in ibd_file:
    line=line.strip()
    l1=line.split('\t')
    ibd_com_set.add(l1[1])
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

print("--------------------")

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


##分为三部分:
#1:共有的org连接共有com
common_org_common_com=[]
common_org_ibd_com=[]
common_org_health_com=[]

ibd_org_ibd_com=[]
ibd_org_common_com=[]

health_org_common_com=[]
health_org_health_com=[]

health_file=open(health_path,'r')
for line in health_file:
    line=line.strip()
    l1=line.split('\t')
    if (l1[1] in health_com_diff) & (l1[0]  in health_spe_diff):
        health_org_health_com.append([l1[0],l1[1]])
    elif l1[0] in health_spe_diff:
        health_org_common_com.append([l1[0],l1[1]])
    elif l1[1] in health_com_diff:
        common_org_health_com.append([l1[0],l1[1]])
    else:
        common_org_common_com.append([l1[0], l1[1]])
health_file.close()

# read IBD file.
ibd_file=open(ibd_path,'r')
for line in ibd_file:
    line=line.strip()
    l1=line.split('\t')
    if (l1[1] in ibd_spe_diff) & (l1[0]  in ibd_com_diff):
        ibd_org_ibd_com.append([l1[0],l1[1]])
    elif l1[0] in ibd_spe_diff:
        ibd_org_common_com.append([l1[0],l1[1]])
    elif l1[1] in ibd_com_diff:
        common_org_ibd_com.append([l1[0],l1[1]])
    else:
        common_org_common_com.append([l1[0], l1[1]])
ibd_file.close()

#1
common_org_common_com_out=open("/home/zc/IDBdata/YY-tu/common_org_common_com_out.csv",'w+')
for arr in common_org_common_com:
    common_org_common_com_out.write("\t".join(arr)+'\n')
common_org_common_com_out.close()
##2
common_org_ibd_com_out=open("/home/zc/IDBdata/YY-tu/common_org_ibd_com_out.csv",'w+')
for arr in common_org_ibd_com:
    common_org_ibd_com_out.write("\t".join(arr)+'\n')
common_org_ibd_com_out.close()
##3
common_org_health_com_out=open("/home/zc/IDBdata/YY-tu/common_org_health_com_out.csv",'w+')
for arr in common_org_health_com:
    common_org_health_com_out.write("\t".join(arr)+'\n')
common_org_health_com_out.close()
#4
ibd_org_ibd_com_out=open("/home/zc/IDBdata/YY-tu/ibd_org_ibd_com_out.csv",'w+')
for arr in ibd_org_ibd_com:
    ibd_org_ibd_com_out.write("\t".join(arr)+'\n')
ibd_org_ibd_com_out.close()
#5
ibd_org_common_com_out=open("/home/zc/IDBdata/YY-tu/ibd_org_common_com_out.csv",'w+')
for arr in ibd_org_common_com:
    ibd_org_common_com_out.write("\t".join(arr)+'\n')
ibd_org_common_com_out.close()
#6
health_org_common_com_out=open("/home/zc/IDBdata/YY-tu/health_org_common_com_out.csv",'w+')
for arr in health_org_common_com:
    health_org_common_com_out.write("\t".join(arr)+'\n')
health_org_common_com_out.close()
#7
health_org_health_com_out=open("/home/zc/IDBdata/YY-tu/health_org_health_com_out.csv",'w+')
for arr in health_org_health_com:
    health_org_health_com_out.write("\t".join(arr)+'\n')
health_org_health_com_out.close()

print("finished")
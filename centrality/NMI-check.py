from collections import Counter
##代码目的:将健康人和IBD聚类以后的结果,把相同的nodes提取出来,计算NMI.判断NMI与不同nodes是否有关.

health_path="/home/zc/IDBdata/IBD-non-species-compound-static/non/spe_comp_wei_spark.txt/part-00000"
ibd_path="/home/zc/IDBdata/IBD-non-species-compound-static/ibd/spe_comp_wei_spark.txt/part-00000"

health_set=set()
ibd_set=set()

# read health file
health_file=open(health_path,'r')
for line in health_file:
    line=line.strip()
    l1=line.split('\t')
    health_set.add(l1[0])
    health_set.add(l1[1])
health_file.close()

ibd_file=open(ibd_path,'r')
for line in ibd_file:
    line=line.strip()
    l1=line.split('\t')
    ibd_set.add(l1[0])
    ibd_set.add(l1[1])
ibd_file.close()
common_set=ibd_set.intersection(health_set)
health_module_file="/home/zc/IDBdata/IBD-non-species-compound-static/non/module_non_ex12_train.txt"
ibd_module_file="/home/zc/IDBdata/IBD-non-species-compound-static/ibd/module_ibd_ex12_train.txt"

health_module_out_file="/home/zc/IDBdata/IBD-non-species-compound-static/non/module_non_ex12_train_nmi.txt"
ibd_module_out_file="/home/zc/IDBdata/IBD-non-species-compound-static/ibd/module_ibd_ex12_train_nmi.txt"


health_module_in=open(health_module_file,"r")
health_module_out=open(health_module_out_file,"w+")
for line in health_module_in:
    line=line.strip()
    node=(line.split("\t"))[0]
    if node in common_set:
        health_module_out.write(line+"\n")
health_module_in.close()
health_module_out.close()

ibd_module_in =open(ibd_module_file,"r")
ibd_module_out=open(ibd_module_out_file,"w+")
for line in ibd_module_in:
    line=line.strip()
    node=(line.split("\t"))[0]
    if(node in common_set):
        ibd_module_out.write(line+"\n")
ibd_module_in.close()
ibd_module_out.close()
print("finished")

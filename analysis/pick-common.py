health_path="/home/zc/IDBdata/three-non5/ex23/module_non_ex23_train.txt"
ibd_path="/home/zc/IDBdata/three-IBD5/ex23/module_ibd_ex23_train.txt"


health_file=open(health_path,'r')
health_set=set()
health_dict={}
for line in health_file:
    line=line.strip()
    lst1=line.split("\t")
    health_set.add(lst1[0])
    health_dict[lst1[0]]=lst1[1]
health_file.close()

ibd_file=open(ibd_path,'r')
ibd_set=set()
ibd_dict={}
for line in ibd_file:
    line=line.strip()
    lst1=line.split("\t")
    ibd_set.add(lst1[0])
    ibd_dict[lst1[0]]=lst1[1]
ibd_file.close()
##交集

inter=ibd_set.intersection(health_set)
print("intersection length")
print(len(inter))
list_inter=sorted(list(inter))
health_list=[]
ibd_list=[]
i=0
for item in list_inter:
    health_list.append([item,health_dict[item]])
    ibd_list.append([item,ibd_dict[item]])
    i=i+1
print(i)
outpath_heal="/home/zc/IDBdata/three-non5/purity&comple/module_non_ex23_train_valicommon.txt"
outpath_ibd="/home/zc/IDBdata/three-non5/purity&comple/module_ibd_ex23_train_valicommon.txt"
wri_hel=open(outpath_heal,'w+')
for line in health_list:
    wri_hel.write("\t".join(line)+'\n')
wri_hel.close()
wri_ibd=open(outpath_ibd,'w+')
for line in ibd_list:
    wri_ibd.write("\t".join(line)+'\n')
wri_ibd.close()
print("finished")
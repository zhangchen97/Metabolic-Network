ibd_path="/home/zc/IDBdata/all_data/ibd-species-filter-filtfile-0.1.csv"
non_path="/home/zc/IDBdata/all_data/non-species-filter-filtfile-0.1.csv"

ibd_file=open(ibd_path,'r')
ibd_specom_set=set()
for line in ibd_file:
    line=line.strip()
    lst1=line.split('\t')
    ibd_specom_set.add(lst1[0])
ibd_file.close()

non_file=open(non_path,'r')
non_specom_set=set()
for line in non_file:
    line=line.strip()
    lst1=line.split('\t')
    non_specom_set.add(lst1[0])
non_file.close()

inter=ibd_specom_set.intersection(non_specom_set)
print("intersection:")
print(len(inter))
ibd_only=ibd_specom_set.difference(non_specom_set)
print("ibd only: ")
print(len(ibd_only))
print(ibd_only)

non_only=non_specom_set.difference(ibd_specom_set)
print("non only:")
print(len(non_only))
print(non_only)

import os,sys
import shutil

def get_sample_typeid(sample_type_id_path):
   infile=open(sample_type_id_path,'r')
   all_dict={}
   for line in infile:
       line=line.strip()
       lst1=line.split('\t')
       key=lst1[1]+'-'+lst1[2]
       all_dict.setdefault(key,set())
       all_dict[key].add(lst1[0])
   #print(all_dict)
   print(len(all_dict))
   return all_dict

##将IBD样本和nonIBD样本分开.
def divide_ibd(inpath,all_dict):
    n=0
    ibd_path="/home/zc/IDBdata/all_data/all-ibd22"
    nonibd_path="/home/zc/IDBdata/all_data/all-non2"
    for person,samples_lst in all_dict.items():
        lst1=person.split("-")
        disease_type =lst1[0]
        if(disease_type=="nonIBD"):
            for sample in samples_lst:
                try:
                    shutil.copy(inpath+'/'+sample+"_taxonomic_profile.tsv",nonibd_path+'/'+sample+"_taxonomic_profile.tsv")
                except:
                    continue
                n=n+1
                print(n)
        else:
            for sample in samples_lst:
                try:
                    shutil.copy(inpath+'/'+sample+"_taxonomic_profile.tsv",ibd_path+'/'+sample+"_taxonomic_profile.tsv")
                except:
                    continue
                n=n+1
                print(n)
    print("finished")
def each_number(all_dict):
    nonibd_count=0
    ibd_count=0
    for person, samples_lst in all_dict.items():
        lst1 = person.split("-")
        disease_type = lst1[0]
        if (disease_type=="nonIBD"):
            nonibd_count+=1
        else:
            ibd_count+=1
    print("nonibd: ",nonibd_count)
    print("ibd: ",ibd_count)


def main():
    sample_type_id_path="/home/zc/IDBdata/sampleid_disease_patientid.txt"
    all_dict=get_sample_typeid(sample_type_id_path)
    print(all_dict)
    #inpath="/home/zc/IDBdata/all_data/all-taxonomy_profiles"
    #divide_ibd(inpath,all_dict)
    each_number(all_dict)
main()

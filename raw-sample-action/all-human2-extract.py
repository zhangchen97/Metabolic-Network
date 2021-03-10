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

##将每个sample分到所属的疾病类型(CD/UC),病人文件下.
def divide_file(all_dict,src_path):
    n=0
    root_path="/home/zc/Downloads/IDBdata/all_sample"
    for person,samples_lst in all_dict.items():
        lst1=person.split("-")
        disease_type =lst1[0]
        person_id=lst1[1]

        #create directory firstly,then copy file to it.
        dir_name=root_path+'/'+disease_type+'/'+person_id
        os.system("mkdir "+dir_name)
        for sample in samples_lst:
            try:
                shutil.copy(src_path+'/'+sample+"_pathabundance.tsv",dir_name+'/'+sample+"_pathabundance.tsv")
            except:
                continue
            n=n+1
            print(n)
    print("finished")

##将IBD样本和nonIBD样本分开.
def divide_ibd(inpath,all_dict):
    n=0
    ibd_path="/home/zc/Downloads/IDBdata/all_sample/IBD-pathway"
    nonibd_path="/home/zc/Downloads/IDBdata/all_sample/nonIBD-pathway"
    for person,samples_lst in all_dict.items():
        lst1=person.split("-")
        disease_type =lst1[0]
        if(disease_type=="nonIBD"):
            for sample in samples_lst:
                try:
                    shutil.copy(inpath+'/'+sample+"_pathabundance.tsv",nonibd_path+'/'+sample+"_pathabundance.tsv")
                except:
                    continue
                n=n+1
                print(n)
        else:
            for sample in samples_lst:
                try:
                    shutil.copy(inpath+'/'+sample+"_pathabundance.tsv",ibd_path+'/'+sample+"_pathabundance.tsv")
                except:
                    continue
                n=n+1
                print(n)
    print("finished")

def main():
    sample_type_id_path="/home/zc/Downloads/IDBdata/sample-type.txt"
    all_dict=get_sample_typeid(sample_type_id_path)
    #all_dict={ 'CD-C3002': {'CSM67UBF', 'CSM5MCVN'}}
    #src_path="/home/zc/Downloads/IDBdata/all_sample/humann2"
    #divide_file(all_dict,src_path)
    inpath="/home/zc/Downloads/IDBdata/all_sample/humann2"
    divide_ibd(inpath,all_dict)
main()




##把pathway.tsv文件从Humann2文件夹里提取出来.
def extract_pathway_file(dir_path):
    dst_path="/home/zc/Downloads/IDBdata/all_sample/humann2"
    lst_dir=os.listdir(dir_path)
    #print(lst_dir)
    n=0
    for single_filename in lst_dir:
        pathway_path=dir_path+'/'+single_filename+'/'+single_filename[0:-7]+"pathabundance.tsv"
        print(pathway_path)
        try:
            shutil.move(pathway_path,dst_path)
        except:
            continue
        n=n+1
        print(n)
    print("finished")
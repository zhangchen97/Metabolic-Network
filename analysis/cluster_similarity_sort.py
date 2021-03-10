import os
import numpy as np
import pandas as pd
def get_cluster(refer_cluster_id,target_filepath):
    target_dict = {}
    target_file = open(target_filepath, "r")
    for line in target_file:
        line = line.strip()
        arr = line.split("\t")
        if (arr[1] not in target_dict.keys()):
            target_dict[arr[1]] = [arr[0]]
        else:
            target_dict[arr[1]].append(arr[0])
    print(target_dict)
    target_index = target_dict.keys()

def main():
    #Non和IBD要分别去考虑,先写Non
    #作为reference的module文件,后续多替换几个
    refer_module_path="/home/zc/IDBdata/IBD-non-species-compound-static/non-module/module_non_ex12_train.txt"
    #比较的存储文件的文件夹目录.
    target_module_dir="/home/zc/IDBdata/IBD-non-species-compound-static/ibd-module"
    #把referencce文件处理一下.
    refer_dict={}
    refer_file=open(refer_module_path,"r")
    for line in refer_file:
        line=line.strip()
        arr=line.split("\t")
        if(arr[1] not in refer_dict.keys()):
            refer_dict[arr[1]]=[arr[0]]
        else:
            refer_dict[arr[1]].append(arr[0])
    #print(refer_dict)
    refer_cluster_id=refer_dict.keys()##cluster_id
    ##将长度不一样的cluster变成一样,填上nan.
    length_max=0
    for cluster in refer_dict.values():
        if(len(cluster))>length_max:
            length_max=len(cluster)
    for cluster in refer_dict.values():
        if(len(cluster)<length_max):
            for i in range(len(cluster),length_max):
                cluster.append(np.nan)
    refer_df=pd.DataFrame.from_dict(refer_dict)
    print(refer_df.head())
    #
    #循环把目标文件夹的文件去比较,然后按照一定顺序保存
    # target_module_files=os.listdir(target_module_dir)
    # for filename in target_module_files:
    #     target_filepath=target_module_dir+"/"+filename
    #     print(target_filepath)
    #     get_cluster(refer_index,target_filepath)
main()
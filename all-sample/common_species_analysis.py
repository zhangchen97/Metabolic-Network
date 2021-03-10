#species sample1 sample2 sample2
#B.coli    0.1    0.2    11
#C.ganvs   11     2.4    3.0
import os
import re
import pandas as pd
def statis_species(filepath,outpath):
    global df_all
    listdir=os.listdir(filepath)
    print(listdir)
    all_sample_count=len(listdir)
    n=0
    for single_file in listdir:
        context = ''
        single_path=filepath+'/'+single_file
        file=open(single_path,'r')
        for line in file:
            context = context + line
        # 找到unclassified的species数量
        pattern1 = re.compile(r's__(.+?)\n')
        species = pattern1.findall(context)
        species_not_t = []
        for line in species:
            if ("|t__" not in line):
                species_not_t.append(line)
        #print(len(species_not_t))
        # list(species pcentage)=>字典（specie,pentage)
        dict = {}
        for specie in species_not_t:
            arr = specie.split("\t")
            dict[arr[0]] = arr[1]
        #print(dict)
        ser=pd.Series(dict,dtype=float)
        df=ser.to_frame()
        df.reset_index(inplace=True)
        df.columns=['species',single_file[0:-22]]
        if(n==0):
            df_all=df
        else:
            df_all=pd.merge(df_all,df,on='species',how='outer')
        n=n+1
        file.close()
    df_all.set_index(["species"], inplace=True)
    ##判断符合条件的species, condition1: 存在一半样本中,且average abundance>0.1
    #print(df_all)
    print("****************")
    df_all['mean']=df_all.mean(axis=1)
    df_all['null_count']=df_all.isnull().sum(axis=1)
    print(df_all.head())
    print("df_all length")
    print(len(df_all))
    df_all1=df_all[df_all['null_count'] < all_sample_count*0.9]
    df_all1=df_all[['mean','null_count']]
    df_all1=df_all1.sort_values(by = ['null_count'],ascending = True)
    print(df_all1.head())
    print(len(df_all1))
    df_all1.to_csv(outpath,sep='\t',header=False)
    print("finished")
def main():
    filepath="/home/zc/IDBdata/all_data/all-taxonomy-nonIBD"
    outpath="/home/zc/IDBdata/all_data/non-species-filter-filtfile-all00.csv"
    statis_species(filepath,outpath)
main()
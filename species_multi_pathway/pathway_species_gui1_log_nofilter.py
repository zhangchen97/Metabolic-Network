import re
import pandas as pd
import os
import numpy as np
from scipy import stats
import math

import time
#func1
#input file format:PWY-7219: adenosine ribonucleotides de novo biosynthesis|g__Bacteroides.s__Bacteroides_vulgatus	0.00632441
#output file format:PWY-7219: adenosine ribonucleotides de novo biosynthesis	Bacteroides_vulgatus	0.01336593
#PSP:   P:pathwayname,S:species name ,P:percent

def pathway_abun(inputdir,outputpath):

    global pathway_specie
    file_list=os.listdir(inputdir)
    print(len(file_list))
    df_all=pd.DataFrame(columns=['A'])
    n = 0#第n个文件
    pattern = re.compile(r'g__.+?s__')

    for file_name in file_list:
        inputfile=os.path.join(inputdir,file_name)
        #print(inputfile)
        sample_name = file_name.split("_")[0]
        input1=open(inputfile,'r')
        #pass掉第一行
        j=0
        dict1={}
        for line in input1:
            line=line.strip()
            arr=line.split("\t")
            if(j>0):
                mid = re.sub(pattern, ",,", arr[0])
                #print(mid)
                id_name=arr[0].split(":")
                if ',,' in mid:
                        str1 = mid.replace("|,,", '\t')
                        pathway_specie=str1.split("\t")

                        path_spe=id_name[0]+'+'+pathway_specie[1]
                        dict1[path_spe]=str(math.log10(float(arr[1]))+6)
            j=j+1
            # 字典转为dataframe
        input1.close()
        ser = pd.Series(dict1,dtype=float)
        df = ser.to_frame()
        df.reset_index(inplace=True)
        df.columns = ["pathway", sample_name]
        if(n==0):
            df_all=df
        else:
            df_all=pd.merge(df_all,df,on="pathway",how='outer')
        n=n+1
        print(n)
    print(df_all.head())
    df_all.set_index(['pathway'],inplace=True)

    ##归一化
    df_all.loc['sum']=df_all.sum(0)
    df_all = df_all.apply(lambda x: x/x['sum'], axis=0)
    df_all=df_all.drop(index=['sum'],axis=0)
    #求均值
    df_all['mean']=df_all.mean(1)
    df_all['std']=df_all.std(1)
    #print(df_all.head())
    df_all['mean']=df_all['mean']
    df_all.reset_index(inplace=True)
    df_all_final=df_all[['pathway','mean']]
    #pathway+species => pathway  species
    df_all_final=pd.concat([df_all_final, df_all_final['pathway'].str.split('+', expand=True)], axis=1, names='species')
    df_out=df_all_final[[0,1,'mean']]
    df_out['mean']=df_out['mean']*10
    print(df_out.head())
    df_out.to_csv(outputpath,header=None,sep='\t',index=None)
    print("finished")


def main():
    inputpath="/home/zc/Auto_Rawdata/Non-IBD (copy)"
    outputpath="/home/zc/IDBdata/IBD-non-species-compound-static/non/path_spe_gui1log.csv"
    pathway_abun(inputpath,outputpath)

main()
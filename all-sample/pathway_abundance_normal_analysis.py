import re
import pandas as pd
import os
from scipy import stats
import math

import time
#func1
#input file format:PWY-7219: adenosine ribonucleotides de novo biosynthesis|g__Bacteroides.s__Bacteroides_vulgatus	0.00632441
#output file format:PWY-7219: adenosine ribonucleotides de novo biosynthesis	Bacteroides_vulgatus	0.01336593
#PSP:   P:pathwayname,S:species name ,P:percent

## explain:
# 不再使用微生物丰度，仅使用pathway的abundance。
def pathway_abun(inputdir,filter_species_path,outputpath):
    ##filter species file
    filter_spe_file=open(filter_species_path,'r')
    filter_speices_set=set()
    for line in filter_spe_file:
        line=line.strip()
        lst=line.split(',')
        filter_speices_set.add(lst[0])
    ##pathway file
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
                        if(pathway_specie[1] in filter_speices_set):
                            path_spe=id_name[0]+'_'+pathway_specie[1]
                            dict1[path_spe]=str(math.log10(float(arr[1])))
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
    df_all['mean']=df_all.mean(1)
    df_all['std']=df_all.std(1)
    df_all['pvalue']=0.0
    print(df_all.head())
    for index,row in df_all.iterrows():
        lst=row.tolist()
        lst2=[]
        for i in lst:
            if(abs(i)>0.0 ):
                lst2.append(i)
        statistic,pvalue=stats.kstest(lst2, 'norm', (row['mean'], row['std']))
        #print(type(pvalue))
        row['pvalue']=pvalue
    df_all=df_all.sort_values(by='pvalue',ascending=False)
    print(df_all.head())
    df_all.to_csv(outputpath)
    print("finished")
def main():
    inputpath="/home/zc/Downloads/IDBdata/all_data/yyfiletest"
    filter_species_path="/home/zc/Downloads/IDBdata/all_data/non-species-filter-filtfile-0.25.csv"
    outputpath="/home/zc/Downloads/IDBdata/all_data/yyresult3.csv"
    pathway_abun(inputpath,filter_species_path,outputpath)

main()
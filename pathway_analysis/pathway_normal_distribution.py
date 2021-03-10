import os
import pandas as pd
from scipy import stats
import math

def pathway_analysis(pathway_file_path,outpath):
    pathway_dir=os.listdir(pathway_file_path)
    file_count=len(pathway_dir)

    count=0
    for single_file in pathway_dir:
        single_path=pathway_file_path+'/'+single_file
        file = open(single_path)
        pathway_dict = {}
        for line in file:
            line =line.strip()
            path_abun=line.split('\t')
            pathway=path_abun[0].split(':')[0]
            if ('|' not in path_abun[0]) & (':' in path_abun[0]):
                #print(path_abun)
                pathway_dict[pathway]=path_abun[1]
        #print(pathway_dict)
        file.close()
        ser=pd.Series(pathway_dict,dtype=float)
        df=ser.to_frame()
        df.reset_index(inplace=True)
        df.columns=['pathway',single_file.split("_")[0]]
        if(count==0):
            df_all=df
        else:
            df_all=pd.merge(df_all,df,how='outer',on='pathway')
        print(count)
        count=count+1
    print(df_all.head())
    print("all pathway counts")
    print(len(df_all))
    df_all.set_index(['pathway'],inplace=True)
    df_all['mean'] = df_all.mean(axis=1)
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
    print(len(df_all))
    df_all.to_csv(outpath,sep='\t')
    print("finished")
def main():
    pathway_file_path="/home/zc/IDBdata/all_data/IBD-pathway-file"
    outpath="/home/zc/IDBdata/all_data/pathway_analysis/ibdpathway_normal.csv"
    pathway_analysis(pathway_file_path,outpath)
main()
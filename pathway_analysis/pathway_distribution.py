import os
import pandas as pd
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

    df_all['null_count']=df_all.isnull().sum(axis=1)
    print(df_all.head())
    print("all pathway counts")
    print(len(df_all))
    #df_all1=df_all[df_all['null_count'] <file_count*(3/4)]
    df_all1=df_all[['pathway','null_count']]
    df_all1=df_all1.sort_values(by = ['null_count'],ascending = True)
    print(df_all1.head())
    print(len(df_all1))
    df_all1.to_csv(outpath,sep='\t',header=False)
    print("finished")
def main():
    pathway_file_path="/home/zc/IDBdata/all_data/nonIBD-pathway-file"
    outpath="/home/zc/IDBdata/all_data/pathway_analysis/nonpathway00.csv"
    pathway_analysis(pathway_file_path,outpath)
main()
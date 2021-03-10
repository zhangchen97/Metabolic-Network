#1：先找到每个sample里abundance大于0.01%的species
#2：讲每个species在每个sample里abundance取平均值。
import re
import pandas as pd
import os
def filter_low_dot1(inputdir,outpath):
    file_list=os.listdir(inputdir)
    df_all=pd.DataFrame(columns=['A'])
    #print(file_list)
    n=0
    for file_name in file_list:
        inputfile=os.path.join(inputdir,file_name)
        sample_name=file_name.split("_")[0]  #MSM6J2HH_taxonomic_profile.tsv   => PSM7J12Z
        #print(inputfile)
        context=''
        file=open(inputfile,'r')
        for line in file:
            context=context+line
        #找到unclassified的species数量
        pattern1=re.compile(r's__(.+?)\n')
        species=pattern1.findall(context)
        species_not_t=[]
        for line in species:
            if("|t__" not in line):
                species_not_t.append(line)
        #print(len(species_not_t))
        #list(species pcentage)=>字典（specie,pentage)
        dict={}
        for specie in species_not_t:
            arr=specie.split("\t")
            if("unclassified" not in arr[0]):
                dict[arr[0]]=arr[1]
        #字典转为dataframe
        ser=pd.Series(dict)
        df=ser.to_frame()
        df.reset_index(inplace=True)
        df.columns=["specie",sample_name]
        df[[sample_name]]= df[[sample_name]].astype(float)
        df2=df.loc[df[sample_name]>0.01]
        if(n==0):
            df_all=df2

        else:
            df_all=pd.merge(df_all,df2,on='specie',how='outer')
        n=n+1
        file.close()
        print(n)
    df_all=df_all.fillna(0)
    df_all['mean']=df_all.mean(axis=1)
    df_all=df_all[['specie','mean']]
    #df_all = df_all.loc[df_all["mean"] > 0.01]
    df_all=df_all.sort_values(['mean'],ascending=False)
    df_all['mean']=df_all['mean']*100
    df_all.to_csv(outpath, sep='\t',index=False,header=False)
    print("finished")


def main():
    filter0dot1_inputdir="/home/zc/IDBdata/all_data/all-taxonomy-IBD"
    filter0dot1_output="/home/zc/IDBdata/all_data/species-analysis/ibd_specie_abun_avebig0.01.csv"
    filter_low_dot1(filter0dot1_inputdir,filter0dot1_output)
main()

# df_final = df_all2.loc[df_all2["average"] > 0.1]
# df_final = df_final.loc[round(df_all2["average"],8)]
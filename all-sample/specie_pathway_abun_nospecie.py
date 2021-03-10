import re
import pandas as pd
import os
import time
#func1
#input file format:PWY-7219: adenosine ribonucleotides de novo biosynthesis|g__Bacteroides.s__Bacteroides_vulgatus	0.00632441
#output file format:PWY-7219: adenosine ribonucleotides de novo biosynthesis	Bacteroides_vulgatus	0.01336593
#PSP:   P:pathwayname,S:species name ,P:percent

## explain:
# 不再使用微生物丰度，仅使用pathway的abundance。
def pathway_abun(inputdir,outputpath):
    file_list=os.listdir(inputdir)
    print(file_list)
    df_all=pd.DataFrame(columns=['A'])
    n = 0
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
                dict1[arr[0]]=str(float(arr[1])*100)
            j=j+1
            # 字典转为dataframe
        input1.close()
        ser = pd.Series(dict1)
        df = ser.to_frame()
        df.reset_index(inplace=True)
        df.columns = ["pathwayspecie", sample_name]
        df[[sample_name]] = df[[sample_name]].astype(float)
        if(n==0):
            df_all=df
            n=n+1
        else:
            df_all=pd.merge(df_all,df,on="pathwayspecie",how='outer')
            n=n+1
        print(n)
    #print(df_all.columns.size)
    df_all.set_index(["pathwayspecie"], inplace=True)
    df_all = df_all.fillna(0)
    mean_series = df_all.sum(axis=1)
    mean_frame = mean_series.to_frame(name='sum')
    mean_frame.reset_index(inplace=True)
    mean_frame.columns = ["pathwayspecie", "sum"]
    df_all.reset_index(inplace=True)
    df_all2 = pd.merge(df_all, mean_frame,on="pathwayspecie",how="outer")
    df_final = df_all2[["pathwayspecie", "sum"]]
    #df_final.set_index(["pathwayspecie"], inplace=True)
    #print(df_final)
    df_new = pd.DataFrame(columns=['pathway_id', 'specie','sum'])
    new_index=0
    for index,row in df_final.iterrows():
        pathspe=row['pathwayspecie']
        #print(pathspe)
        mid = re.sub(pattern, ",,", pathspe)
        # PSP:   P:pathwayname,S:species name ,P:percent
        if ',,' in mid:
            str1 = mid.replace("|,,", '\t')
            pathway_specie=str1.split("\t")
            str2 = pathway_specie[0].split(":")
            df_new = df_new.append([{'pathway_id': str2[0],'specie':pathway_specie[1],'sum':row['sum']}], ignore_index=True)
            new_index=new_index+1

    df_new.set_index(["pathway_id"], inplace=True)
    df_new.to_csv(outputpath,sep="\t",header=False)
    print("finished")
#species's pathway dictionary
def all_pathway_dict(inpath,outpath):
    file=open(inpath,'r')
    all_pathway=set()
    for line in file:
        line=line.strip()
        pathway=line.split("\t")[0]
        all_pathway.add(pathway)
    file.close()
    context='\n'.join(all_pathway)
    outfile=open(outpath,'w+')
    outfile.write(context)
    print(" all pathway's dictionary finished")

# all pathway of each specie
def species_pathway(inputpath,outpath):
    file=open(inputpath,'r')
    dict1={}
    pathwayset=set()
    for line in file:
        list1=line.split('\t')
        dict1.setdefault(list1[2], set()) #添加个空set
        dict1[list1[2]].add(list1[0])
        pathwayset.add(list1[0])
    print(dict1)
    print(len(pathwayset))  #pathway的总数量
    outputfile=open(outpath,'w+')
    for k,v in dict1.items():
        for v1 in v:
            outputfile.write(k+'\t'+v1+'\n')
    print(len(dict1))
    file.close()
    outputfile.close()

def main():
    inputpath="/home/zc/IDBdata/three-Non/ex23/data-test"
    outputpath="/home/zc/IDBdata/three-Non/ex23/mid-test/pathway_idname_specie_ave.txt"
    pathway_abun(inputpath,outputpath)
    #time.sleep(15)
    #pathway_dict_inpath="/home/zc/IDBdata/all_sample/IBD-trial4/mid-test/pathway_idname_specie_ave.txt"
    #pathway_dict_outpath="/home/zc/IDBdata/all_sample/IBD-trial4/mid-test/all_pathway_dict.txt"
    #all_pathway_dict(pathway_dict_inpath,pathway_dict_outpath)

    sp_inputpath="/home/zc/Downloads/IDBdata/10-sample/pathway_idname_specie_ave.txt"
    sp_outpath="/home/zc/Downloads/IDBdata/10-sample/pathway_of_specie.txt"
    #species_pathway(sp_inputpath,sp_outpath)
main()
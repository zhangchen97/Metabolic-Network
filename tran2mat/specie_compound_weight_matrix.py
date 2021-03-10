import pandas as pd

def get_matrix(inpath,outpath):
    infile=open(inpath,'r')
    specie_compound_list=[]
    specie_set=set()
    for line in infile:
        line=line.strip()
        list1=line.split("\t")
        specie_set.add(list1[0])
        list1[2]=float(list1[2])*100
        specie_compound_list.append(list1)
    infile.close()
    specie_list=list(specie_set)

    all_spe_lst_com_abun=[]

    for specie in specie_list:
        spe_lst_com_abun = []
        spe_lst_com_abun.append(specie)
        for lst1 in specie_compound_list:
            if specie==lst1[0]:
                com_abun=[]
                com_abun.append(lst1[1])
                com_abun.append(lst1[2])
                spe_lst_com_abun.append(com_abun)
        all_spe_lst_com_abun.append(spe_lst_com_abun)
    print(len(all_spe_lst_com_abun))
    #print(all_spe_lst_com_abun)
    n=0
    for lst1 in all_spe_lst_com_abun:
        #if(n<2):
            i=0
            com_lst=[]
            weight_lst=[]
            for ele in lst1: #['Bacteroides_vulgatus', ['L-alanine', '59.5050977113152'], ['(S)-2-acetolactate', '55.61537446962561']
                if(i>0):
                    com_lst.append(ele[0])
                    weight_lst.append(ele[1])
                i=i+1
            df1 = pd.DataFrame(weight_lst,index=com_lst, columns=[lst1[0]])
            df1.reset_index(inplace=True)
            df1.columns=['compound',lst1[0]]
            #print(df1)
            if(n==0):
                df_all=df1
            else:
                df_all=pd.merge(df_all,df1,on='compound',how='outer')
            n=n+1
            print(n)
        #else:
            #break
    #print(df_all)
    df_all=df_all.fillna(0)
    df_all.to_csv(outpath+".csv",sep='\t')
    df_all.set_index(['compound'],inplace=True)
    #print(df_all.head())
    df_all.to_csv(outpath+"_lpa.csv",sep='\t',index=0,header=0)
    print(df_all.head())
    index_file=open(outpath[:-6]+"index.txt",'w+')
    index=list(df_all.index)
    col=list(df_all.columns)
    for i in range(len(index)):
        if(i<len(col)):
            string=str(i)+'\t'+index[i]+'\t'+col[i]+'\n'
        else:
            string = str(i) + '\t' + index[i] + '\n'
        index_file.write(string)
    index_file.close()

    print(index)
    print(col)
    print("finished")

def main():
    inpath="/home/zc/IDBdata/three-non5-23/ex12/mid-test/spe_comp_wei_spark.txt/part-00000"
    outpath="/home/zc/IDBdata/three-non5-23/ex12/mid-test/non_ex12_test_matrix"
    get_matrix(inpath,outpath)
main()
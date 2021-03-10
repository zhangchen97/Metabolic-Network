import os
from sklearn.model_selection import KFold
import numpy as np
import random, shutil
import re
import pandas as pd
import os
import numpy as np
import math
import time
import sys
##脚本运行格式 python integrate.py start end
#start=eval(sys.argv[1])
#end=eval(sys.argv[2])
#首先是两个文件夹,第一个Auto_Rawdata保存原始的文件;第二个Auto_Meta保存每次循环的文件
raw_path="/home/zc/Auto_Rawdata"
iter_path="/home/zc/Auto_Meta"
start=1
end=3
def main():
    ############1:自动生成3组交叉验证文件##################
    # 遍历 先尝试2次
    for times in range(start,end):
        os.chdir(iter_path)  ##改变目录
        print(os.getcwd())   ##取得当前工作目录
        subfile_name="trial"+str(times)
        os.mkdir(subfile_name)
        os.chdir(iter_path+"/"+subfile_name)
        print(os.getcwd())
        #产生交叉验证的文件分类
        #non-ibd
        non_list_file=np.array(os.listdir("/home/zc/Auto_Rawdata/Non-IBD"))
        random.shuffle(non_list_file)#打乱
        list_n=np.array(range(1,len(non_list_file)+1))
        #print(non_list_file)
        kf = KFold(n_splits=3)
        k_each = 1
        nmi_list=[]

        for train_index, test_index in kf.split(list_n):
            #print("TRAIN:", train_index, "TEST:", test_index)
            X_train, X_test = non_list_file[train_index], non_list_file[test_index]
            #y_train, y_test = list_n[train_index], list_n[test_index]
            #print(X_train)  #作为训练集的文件
            #print(X_test)   #作为测试集的文件
            os.mkdir("non-"+str(k_each)+"-train")
            os.mkdir("non-" + str(k_each)+"-test")
            moveFile(X_train, X_test,"non",k_each)#复制转移文件
            #开始生成图数据
            call_func("non", k_each, "train")
            #聚类后生成module文件
            module("non",k_each,"train")

            call_func("non", k_each, "test")
            module("non", k_each, "test")
            keyfilepath=os.getcwd()+"/module"+"-non-"+str(k_each)+"-train.txt"
            annotatepath=os.getcwd()+"/module"+"-non-"+str(k_each)+"-test.txt"
            nonnmi=nmi(keyfilepath, annotatepath)
            k_each=k_each+1
            nmi_list.append(nonnmi)
        #ibd生成数据
        ibd_list_file = np.array(os.listdir("/home/zc/Auto_Rawdata/IBD"))
        random.shuffle(ibd_list_file)  # 打乱
        list_n = np.array(range(1, len(ibd_list_file) + 1))
        #print(ibd_list_file)
        kf = KFold(n_splits=3)
        k_each = 1
        for train_index, test_index in kf.split(list_n):
            #print("TRAIN:", train_index, "TEST:", test_index)
            X_train, X_test = ibd_list_file[train_index], ibd_list_file[test_index]
            # y_train, y_test = list_n[train_index], list_n[test_index]
            #print(X_train)  # 作为训练集的文件
            #print(X_test)  # 作为测试集的文件
            os.mkdir("ibd-" + str(k_each)+"-train")
            os.mkdir("ibd-" + str(k_each)+"-test")
            moveFile(X_train, X_test, "ibd", k_each)  ##复制转移文件
            ##############################2:产生图数据#######################
            call_func("ibd", k_each, "train")
            module("ibd", k_each, "train")

            call_func("ibd", k_each, "test")
            module("ibd", k_each, "test")
            keyfilepath=os.getcwd()+"/module"+"-ibd-"+str(k_each)+"-train.txt"
            annotatepath=os.getcwd()+"/module"+"-ibd-"+str(k_each)+"-test.txt"
            ibdnmi=nmi(keyfilepath, annotatepath)
            nmi_list.append(ibdnmi)
            k_each = k_each + 1
        for k_each in range(1,4):
             keyfilepath = os.getcwd() + "/module" + "-non-" + str(k_each) + "-train.txt"
             annotatepath = os.getcwd() + "/module" + "-ibd-" + str(k_each) + "-train.txt"
             non_ibd_nmi = nmi(keyfilepath, annotatepath)
             nmi_list.append(non_ibd_nmi)    #此时nmi_list=[non1,non2,non3,ibd1,ibd2,ibd3,non-ibd1,non-ibd2,non-ibd3]
         #存储这次time的NMI结果
        nmi_file = open(iter_path + "/" + str(start) + "-" + str(end) + "-result.txt", 'w+')
        for k_each in range(0, 3):
                    #  k_each      non_nmi              ibd_nmi        non_ibd_nmi
             string=str(times)+"-"+str(k_each+1)+"\t"+str(nmi_list[k_each])+"\t"+str(nmi_list[k_each+3])+"\t"+str(nmi_list[k_each+6])+"\n"
             nmi_file.write(string)
        nmi_file.close()
        print("count: "+str(times))


##########################2生成图###################################

def call_func(type,k_each,data_type):#type是non或者ibd   data_type是train 或者test
    inputpath = os.getcwd() + "/" + type + "-"+ str(k_each)+"-"+data_type
    df_out = pathway_abun(inputpath)
    if (type == "non"):
        specie_abun_path = "/home/zc/Auto_Rawdata/allnon_specie_abudance_ave.csv"
    elif (type == "ibd"):
        specie_abun_path = "/home/zc/Auto_Rawdata/allibd_specie_abudance_ave.csv"
    #specie_abun_path = "/home/zc/Auto_Rawdata/allnon_specie_abudance_ave.csv"
    all_filter_pathway_compound_path = "/home/zc/Auto_Rawdata/all-pathway-compound-filter1.txt"
    specie_pathway_abun = get_specie_pathway_abun(specie_abun_path, df_out)
    spe_com_wei = get_speice_compound_weight(specie_pathway_abun, all_filter_pathway_compound_path)
    outpath = os.getcwd()+"/"+str(type)+"-"+str(k_each)+"-"+data_type+"-matrix"
    get_matrix(spe_com_wei, outpath)
    time.sleep(20)
    ###################################3:聚类##############################
    cluster(type,data_type,k_each)

def cluster(type,data_type,k_each):
    inpath=os.getcwd()+"/"+str(type)+"-"+str(k_each)+"-"+data_type+"-matrix-lpa.csv"
    outpath=os.getcwd()+"/res-"+str(type)+"-"+str(k_each)+data_type+".txt"
    cmd="julia /home/ubuntu/Auto_Rawdata/julia_main.jl "+inpath+" "+outpath
    os.system(cmd)

    ######################################5:计算NMI################################
def nmi(keyfilepath,annotatepath):
    keyfile = keyfilepath
    keyinfo = get_annotated_key(keyfile)
    #print(keyinfo)
    config1 = annotate_clusters(annotatepath,keyinfo)
    nmi, ii = get_nmi(config1)
    return nmi
    #############################4:聚类后生成module文件################################################
def module(type,k_each,data_type):
    index_path=os.getcwd()+"/"+str(type)+"-"+str(k_each)+"-"+data_type+"-index.txt"
    specie_dict,compound_dict=spe_com_index(index_path)
    lpa_index_path=os.getcwd()+"/"+str(type)+"-"+str(k_each)+"-"+str(data_type)+"-matrix-lpa.txt"
    outpath=os.getcwd()+"/module-"+str(type)+"-"+str(k_each)+"-"+data_type+".txt"
    lpa_index(lpa_index_path,specie_dict,compound_dict,outpath)
    time.sleep(20)
def moveFile(train,test,type,k_each):
    if(type=="ibd"):
        fileDir="/home/zc/Auto_Rawdata/IBD/"
    else:
        fileDir = "/home/zc/Auto_Rawdata/Non-IBD/"
    for name in train:
        tarDir = os.getcwd() +"/"+ type+"-"+ str(k_each)+"-train" +'/'
        shutil.copy(fileDir + name, tarDir + name)
    for name in test:
        tarDir = os.getcwd() +"/"+ type+"-"+ str(k_each)+"-test" +'/'
        shutil.copy(fileDir + name, tarDir + name)

def get_annotated_key(keyfile):
    keyinfo = {}
    if not (os.path.exists(keyfile)):
        print("at least one of the input files are not found.")
        sys.exit(0)
    with open(keyfile, 'r') as KEY:
        for lines in KEY:  # .readlines():
            try:
                anarray = lines.strip("\n").split("\t")
                keyinfo[anarray[0]] = anarray[1]  # there was an extra >
            except:
                continue
    KEY.close()
    #print("Number of reads in the annotation: " + '{:,d}'.format(len(keyinfo.keys())))
    known_clusters = pd.DataFrame.from_dict(keyinfo, 'index')
    known_clusters = known_clusters.rename(columns={0: 'transcript'})
    known_counts = known_clusters.groupby(['transcript']).size()
    #print("Total reads in annotated clusters: " + '{:,d}'.format(known_counts[known_counts > 1].sum()))
    #print("Total annotated clusters: " + '{:,d}'.format(sum(known_counts > 1)))
    #print("The top 10 biggest annotated clusters are:")
    #print(known_counts.sort_values(ascending=False)[0:10])
    return keyinfo

def annotate_clusters(cluster, annotations):
    '''
    parse spark cluster results
    cluster file format is: seqid \t cluster_id
    return: [seq_name, cluster_id, annotation_transcript]
    '''
    if not os.path.exists(cluster):
        print("Cluster file not found.")
        sys.exit(0)

    results = []
    total_clustered_reads = 0
    total_clustered_annotated = 0
    with open(cluster, 'r') as IN:
        for lines in IN:  # .readlines():
            seq_id, group_id = lines.strip("\n").split("\t")
            total_clustered_reads += 1
            try:
                if int(group_id) > 0 and annotations[seq_id] != 'na':
                    results.append([seq_id, group_id, annotations[seq_id]])
                    total_clustered_annotated += 1
            except:
                continue
    IN.close()
    #print("Total reads in clusters: " + '{:,d}'.format(total_clustered_reads))
    #print("Total annotated reads in clusters: " + '{:,d}'.format(total_clustered_annotated))
    return pd.DataFrame(results)

def get_nmi(config):
    cluster_ids = set(config[1])
    data = []
    for name, group in config.groupby([2]):
        d = {c: 0 for c in cluster_ids}
        for g in group[1]:
            d[g] += 1
        d.pop('-1', None)  # remove unclustered reads
        data.append([d[k] for k in sorted(d.keys())])
    data = np.array(data).astype(float)
    tc = np.copy(data)
    tcp = tc / np.sum(tc)
    ws = [np.sum(tc[i]) / (np.sum(tc) + 0.0000000000001) for i in range(len(tc))]
    cs = [np.sum(np.transpose(tc)[i]) / (np.sum(tc) + 0.0000000000001) for i in range(len(np.transpose(tc)))]
    if len(ws) > 1 and len(cs) > 1:
        II = 0
        for i in range(len(ws)):
            for j in range(len(cs)):
                II += tcp[i][j] * np.log((tcp[i][j]) / (cs[j] * ws[i] + 0.0000000000001) + 0.000000000001)
        Hc = np.sum([-csi * np.log(csi + 0.000000000001) for csi in cs])
        Hw = np.sum([-cwi * np.log(cwi + 0.000000000001) for cwi in ws])
        H = (Hc + Hw) * 0.5
        NMI = II / H
        return NMI, II
    else:
        return 'len 1'

##||ff
def spe_com_index(index_path):
    index_file=open(index_path,"r")
    specie_dict={}
    compound_dict={}
    for line in index_file:
        line=line.strip()
        lst1=line.split("\t")
        if len(lst1)==3:
            specie_dict[lst1[0]]=lst1[2]
            compound_dict[lst1[0]]=lst1[1]
        elif  len(lst1)==2:
            compound_dict[lst1[0]] = lst1[1]
        else:
            print("error")
            #print(lst1)
            break
    index_file.close()
    return specie_dict,compound_dict
def lpa_index(lpa_index_path,specie_dict,compound_dict,outpath):
    lpa_file=open(lpa_index_path,'r')
    rows=0
    spe_index=[]
    lpa_spe_index=[]
    com_index=[]
    lpa_com_index=[]
    for line in lpa_file:
        line=line.strip()
        line=line[1:-1]
        lst1=line.split(",")
        if rows==0:
            com_index = lst1
        elif rows==1:
            lpa_com_index = lst1
        elif rows==2:
            spe_index=lst1
        elif rows==3:
            lpa_spe_index = lst1
        rows=rows+1
    outfile=open(outpath,'w+')
    if(len(lpa_spe_index)!=len(spe_index)):
        print("error")
        #print(len(lpa_spe_index))
        #print(len(spe_index))
    for i in range(len(spe_index)):
        #print(i)
        line1=specie_dict[str(int(spe_index[i])-1)]+'\t'+(lpa_spe_index[i])+'\n'
        outfile.write(line1)
    if (len(lpa_com_index) != len(com_index)):
        print("error")
    for j in range(len(com_index)):
        line2 = compound_dict[str(int(com_index[j])-1)] + '\t' + str(int(float(lpa_com_index[j])))+'\n'
        outfile.write(line2)
    lpa_file.close()
    outfile.close()

##||ff
def pathway_abun(inputdir):
    global pathway_specie
    file_list=os.listdir(inputdir)
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
    #print(df_all.head())
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
    return  df_out

def get_specie_pathway_abun(specie_abun_path,df_out):
    specie_abun_file=open(specie_abun_path,'r')
    specie_abun={}
    for line in specie_abun_file:
        line=line.strip()
        list1=line.split("\t")
        specie_abun[list1[0]]=list1[1]
    specie_abun_file.close()

    specie_pathway_abun_data = df_out.values.tolist()
    specie_pathway_abun=[]
    for line in specie_pathway_abun_data:
        single_list=[]
        single_list.append(line[0])
        single_list.append(line[1])
        single_list.append(float(line[2]))
        specie_pathway_abun.append(single_list)
    #print(specie_pathway_abun)
    for single_spw in reversed(specie_pathway_abun):
        if single_spw[1] in specie_abun.keys():
            single_spw[2]=float(specie_abun[single_spw[1]])*single_spw[2]*100
        else:
            #print(specie_pathway_abun.index(single_spw))
            del specie_pathway_abun[specie_pathway_abun.index(single_spw)]
    return specie_pathway_abun


def get_speice_compound_weight(specie_pathway_abun,pathway_compound):

    all_path_com_file=open(pathway_compound,'r')
    pathway_compound=[]
    for line in all_path_com_file:
        single_path_com=[]
        line=line.strip()
        lst=line.split('\t')
        single_path_com.append(lst[0])
        single_path_com.append(set(lst[1:]))
        pathway_compound.append(single_path_com)
    all_path_com_file.close()
    #print(pathway_compound)
    all_com_spe_abun = []
    for p_s_a in specie_pathway_abun:  # ['PWY-7219', 'Bacteroides_vulgatus', 39.7613957497792]
        for p_c in pathway_compound:  # ['PWY-6892', {'2-[(2R,5Z)-2-carboxy-4-methylthiazol-5(2H)-ylidene]ethyl phosphate', 'L-cysteine']
            if p_s_a[0] == p_c[0]:
                for c in p_c[1]:
                    each_com_spe_abun = []
                    each_com_spe_abun.append(p_s_a[1])
                    each_com_spe_abun.append(c)
                    each_com_spe_abun.append(p_s_a[2])
                    all_com_spe_abun.append(each_com_spe_abun)

    # print(all_com_spe_abun)##[['Burkholderiales_bacterium_1_1_47', 'AMP', 0.00237682054168], ['Burkholderiales_bacterium_1_1_47', 'XMP', 0.00237682054168]]
    #print(len(all_com_spe_abun))
    df = pd.DataFrame(all_com_spe_abun, columns=['speices', 'compound', 'weight'])
    df2 = df.groupby(['speices', 'compound'])["weight"].sum()
    df2 = df2.to_frame()
    df2.to_csv("/home/zc/IDBdata/three-non5-总文件/three-non5-211/ex12/spe_comp_wei_spark.csv",sep="\t",header=None)
    return df2

def get_matrix(spe_com_wei,outpath):
    spe_com_wei.reset_index(inplace=True)
    infile = spe_com_wei.values.tolist()
    specie_compound_list=[]
    specie_set=set()
    for line in infile:
        #print(line)
        specie_set.add(line[0])
        line[2]=float(line[2])*100
        specie_compound_list.append(line)
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
            #print(n)
        #else:
            #break
    #print(df_all)
    df_all=df_all.fillna(0)
    df_all.to_csv(outpath+".csv",sep='\t')
    df_all.set_index(['compound'],inplace=True)
    #print(df_all.head())
    df_all.to_csv(outpath+"-lpa.csv",sep='\t',index=0,header=0)
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

main()
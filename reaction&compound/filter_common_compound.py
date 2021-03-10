'''
reaction1 compound1 compound2 ....
=>reaction1 compound1
  reaction2 compound2
  ...
'''
##
def trans_format(inpath,outpath):
    infile=open(inpath,'r')
    outfile=open(outpath,'w+')
    filter1_list=["H2O","ATP","H+","CO2","dATP","ATP", "H2" ,"H2CO3" , "H2O2" ,"H2S",
                 "NAD+", "NADH","NH3",  "O2" ,"NADPH", "NADP+","phosphate","diphosphate",
                 "oxygen","H+[in]","H+[out]","NADH[in]","NAD+[in]",
                 "Nitrate", "Nitricoxide", "Nitrite", "Sulfate","Sulfite","L-glutamate","Phosphate","Pyrophosphate"]

    filter2_list=["H2O","ATP","H+","CO2","dATP","dADP","ADP", "H2" ,"H2CO3" , "H2O2" ,"H2S",
                 "NAD+", "NADH","NH3",  "O2" ,"NADPH","NADP+", "NADP+", "NADPH","phosphate","diphosphate",
                 "oxygen","H+[in]","H+[out]","NADH[in]","NAD+[in]","AMP","UDP","NAD(P)H","IMP","GTP","GDP"]
                 #结果很差

    filter3_list=["H2O","ATP","H+","CO2","dATP","dADP","ADP", "H2" ,"H2CO3" , "H2O2" ,"H2S",
                 "NAD+", "NADH","NH3","O2" ,"NADPH","NADP+","phosphate","diphosphate",
                 "oxygen","H+[in]","H+[out]","NADH[in]","NAD+[in]","AMP","UDP","NAD(P)H","IMP","GTP","GDP",
                 "nitrate", "Nitricoxide", "nitrite", "sulfate","sulfite","L-glutamate","Phosphate","Pyrophosphate",
                  "H2O[periplasm]","H2O[in]","H2O[extracellular space]","oxygen[in]","H+[periplasm]","H+[cytosol]",
                  "NAD(P)+"
                  ]
    #filter_list=[""]
    for line in infile:
        line=line.strip()
        list=line.split('\t')
        n=0
        #print(line)
        for i in list:
            flag = 0
            if(n>0):
               for filter_com in filter3_list:
                   if filter_com==i:
                        flag=1
               if flag==0:
                   outfile.write(list[0] + '\t' + i + '\n')
            n=n+1
    outfile.close()
    infile.close()
    print("finished")
def main():
    inpath="/home/zc/IDBdata/all-reaction-compound.txt"
    outpath="/home/zc/IDBdata/all_filter_common_compound-filter3.txt"
    trans_format(inpath,outpath)
main()

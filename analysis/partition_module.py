
##将LPAWB+得到的数据进一步处理，得到
## module1:(species:[specie1,specie2,...,specie n],compound:[compound1,compound2,...,compound n])

# species compound index
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
            print(lst1)
            break
    index_file.close()
    print(len(specie_dict))
    print(specie_dict)
    print(len(compound_dict))
    print(compound_dict)
    print("finished")
    return specie_dict,compound_dict
    '''
    ROW_IX = sortperm(vec(OUT[1]));
    COL_IX = sortperm(vec(OUT[2]));
    ROWS = OUT[1][ROW_IX];
    COLS = OUT[2][COL_IX];
    MODU=OUT[3]
    write_file={ROW_IX,ROWS,COL_IX,COLS,MODU}
    writedlm(PATH,write_file,'\t')
    print("writing finished")
    '''

def lpa_index(lpa_index_path,specie_dict,compound_dict,outpath=""):

    lpa_file=open(lpa_index_path,'r')
    rows=0
    spe_index=[]
    lpa_spe_index=[]
    com_index=[]
    lpa_com_index=[]
    for line in lpa_file:
        line=line.strip()
        line=line[1:-1]
        print(line)
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
        print(len(lpa_spe_index))
        print(len(spe_index))
    #outfile.write("species-start\n")
    for i in range(len(spe_index)):
        print(i)
        line1=specie_dict[str(int(spe_index[i])-1)]+'\t'+(lpa_spe_index[i])+'\n'
        outfile.write(line1)

    if (len(lpa_com_index) != len(com_index)):
        print("error")
    #outfile.write("compound-start\n")
    for j in range(len(com_index)):
        line2 = compound_dict[str(int(com_index[j])-1)] + '\t' + str(int(float(lpa_com_index[j])))+'\n'
        outfile.write(line2)
    lpa_file.close()
    outfile.close()
    print("finished")
def main():
    index_path="/home/zc/IDBdata/three-non5-22/ex12/mid-test/non_ex12_test_index.txt"
    specie_dict,compound_dict=spe_com_index(index_path)

    lpa_index_path="/home/zc/IDBdata/three-non5-22/three-non5-22/res-non_ex12_test.txt"
    outpath="/home/zc/IDBdata/three-non5-22/three-non5-22/module_non_ex12_test.txt"
    lpa_index(lpa_index_path,specie_dict,compound_dict,outpath)

main()

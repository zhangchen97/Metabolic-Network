def compound_union(inpath1,inpath2,outpath):
    infile1=open(inpath1)
    reaction_set1=set()
    reaction_compoundall=[]
    for line in infile1:
        line=line.strip()
        lst1=line.split("\t")
        reaction_compoundall.append(lst1)
        reaction_set1.add(lst1[0])
    infile1.close()

    infile2=open(inpath2)
    reaction_set2 = set()
    reaction_compound2 = []
    for line in infile2:
        line=line.strip()
        lst1=line.split("\t")
        reaction_compound2.append(lst1)
        reaction_set2.add(lst1[0])
    infile2.close()
    reaction_diff=reaction_set2.difference(reaction_set1)
    if(len(reaction_diff)>0):
        for reaction in reaction_diff:
            for reac_com in reaction_compound2:
                    if(reac_com[0]==reaction):
                        reaction_compoundall.append(reac_com)
    else:
        print("no different reaction")
        return 0
    writefile=open(outpath,'w+')
    for lst in reaction_compoundall:
        string="\t".join(lst)+'\n'
        writefile.write(string)
    writefile.close()
    print("finished")
def main():
    inpath1="/home/zc/Downloads/IDBdata/all-reaction-compound3.txt"
    inpath2 = "/home/zc/Downloads/IDBdata/all_sample/IBD-trial1/test-mid-file/compound_each_reaction.txt"
    outpath="/home/zc/Downloads/IDBdata/all-reaction-compound4.txt"
    compound_union(inpath1,inpath2,outpath)
main()
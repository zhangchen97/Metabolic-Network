def map_func(all_com_inpath,pathway_reac_path,outpath):
    all_com_file=open(all_com_inpath,'r')
    all_reaction_set=set()
    all_reacion_com=[]
    for line in all_com_file:
        line =line.strip()
        lst1=line.split("\t")
        all_reacion_com.append(lst1)
        all_reaction_set.add(lst1[0])
    all_com_file.close()

    pathway_reac_file=open(pathway_reac_path,'r')
    new_reaction_set=set()
    for line in pathway_reac_file:
        line=line.strip()
        lst1=line.split("\t")
        n=0
        for i in lst1:
            if(n>0):
                new_reaction_set.add(i)
            n=n+1
    reaction_differ=new_reaction_set.difference(all_reaction_set)

    new_reaction_com=[]
    for reaction in new_reaction_set:
        for reac_com in all_reacion_com:
            if(reaction==reac_com[0]):
                new_reaction_com.append(reac_com)
    outfile=open(outpath,'w+')
    for item in new_reaction_com:
        stirng="\t".join(item)+'\n'
        outfile.write(stirng)
    outfile.close()
    print("map finished")

def main():
    all_com_inpath="/home/zc/Downloads/IDBdata/all-reaction-compound4.txt"
    pathway_reac_path="/home/zc/Downloads/IDBdata/experiment5-non-vali/mid-test/reaction_each_pathway.txt"
    outpath="/home/zc/Downloads/IDBdata/experiment5-non-vali/mid-test/compound_each_reaction.txt"
    map_func(all_com_inpath,pathway_reac_path,outpath)
main()
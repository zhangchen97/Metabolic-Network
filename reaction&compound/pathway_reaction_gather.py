
def deal(all_path,new_path,outpath):
    all_file = open(all_path,'r')

    all_pathway_set=set()
    all_pathway_reaction_list=[]
    for line in all_file:
        line=line.strip()
        lst1=line.split("\t")
        all_pathway_set.add(lst1[0])
        all_pathway_reaction_list.append(lst1)
    all_file.close()

    new_file = open(new_path,'r')
    new_pathway_set = set()
    new_pathway_reaction_list = []
    for line in new_file:
        line = line.strip()
        lst1 = line.split("\t")
        new_pathway_set.add(lst1[0])
        new_pathway_reaction_list.append(lst1)
    new_file.close()
    pathway_diff=new_pathway_set.difference(all_pathway_set)
    if(len(pathway_diff)==0):
        print("no new pathway")
        return 0
    else:
        for pathway in pathway_diff:
            for lst in new_pathway_reaction_list:
                if(lst[0]==pathway):
                    all_pathway_reaction_list.append(lst)
    outfile=open(outpath,'w+')
    for lst in all_pathway_reaction_list:
        string="\t".join(lst)+'\n'
        outfile.write(string)
    outfile.close()
    print("finished")
def main():
    all_path="/home/zc/Downloads/IDBdata/all_pathway_reaction.txt"
    new_path="/home/zc/Downloads/IDBdata/all_sample/nonIBD-trial1/test-mid-file/reaction_each_pathway.txt"
    outpath="/home/zc/Downloads/IDBdata/all_pathway_reaction2.txt"
    deal(all_path,new_path,outpath)
main()
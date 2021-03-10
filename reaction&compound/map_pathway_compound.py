
#reaction of each pathway
#compound of each reaction
# map them.
def get_pathway_compound(pathway_reaction_path, reaction_compound_path,outpath):
    pathway_reaction = []
    pathway_reaction_file = open(pathway_reaction_path, 'r')
    for line in pathway_reaction_file:             # PWY-6892	RXN-9789	RXN-11319	DXS-RXN	RXN-14382
        line = line.strip()
        list1 = line.split("\t")
        pathway_reaction.append(list1)
    pathway_reaction_file.close()
    # print(pathway_reaction)

    ##read reaction_compound file
                                                                 #PEPSYNTH-RXN	phosphoenolpyruvate
    reaction_compound_file = open(reaction_compound_path, 'r')   #PEPSYNTH-RXN	AMP
    filter_reaction_compound_List = []                           #PEPSYNTH-RXN	pyruvate
    for line in reaction_compound_file:
        line = line.strip()
        list2 = line.split("\t")
        filter_reaction_compound_List.append(list2)
    # print(filter_reaction_compound_List)
    reaction_compound_file.close()
    all_pathway_compound = []

    for path_reac in pathway_reaction:
        i = 0  # 因为path_reac第一个元素是pathway，所以要排除。
        each_pathway_compound = []
        compound_set = set()
        for reaction in path_reac:  ##['PWY-6892', 'RXN-9789', 'RXN-11319', 'DXS-RXN']
            if (i == 0):
                each_pathway_compound.append(reaction)  ##将pathway存入each_pathway_compound的0位置。
                i = i + 1
            else:
                for reac_com in filter_reaction_compound_List:
                    if reac_com[0] == reaction:
                        compound_set.add(reac_com[1])
                i = i + 1
        each_pathway_compound.append(compound_set)
        all_pathway_compound.append(each_pathway_compound)
    print(all_pathway_compound)
    print(len(all_pathway_compound))
    pathway_set = set()
    com_set = set()
    n = 0
    for i in all_pathway_compound:
        pathway_set.add(i[0])
        com_set = com_set.union(i[1])
        n = n + len(i[1])
    print("pathway set count:" + str(len(pathway_set)))
    print("compound set count:" + str(len(com_set)))
    print(n)
    print("get_pathway_compound finished")
    print(all_pathway_compound)
    outfile=open(outpath,'w+')
    for lst in all_pathway_compound:
        string =lst[0]+'\t'+'\t'.join(lst[1])+'\n'
        outfile.write(string)
    outfile.close()
    print("finished")

def main():
    all_reac_com_path = "/home/zc/IDBdata/all_filter_common_compound-filter3.txt"

    all_pathway_reac_path="/home/zc/IDBdata/all_pathway_reaction.txt"
    outpath="/home/zc/IDBdata/all-pathway-compound-filter3.txt"
    get_pathway_compound(all_pathway_reac_path,all_reac_com_path,outpath)
main()
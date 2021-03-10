# pathwayid,specie_name,abundance
# pathway_set()
def get_specie_pathway_abun(pathway_specie_pathabun_path):
    specie_pathway_abun_file = open(pathway_specie_pathabun_path, 'r')
    specie_pathway_abun = []
    for line in specie_pathway_abun_file:
        line = line.strip()
        single_list = []
        list2 = line.split("\t")
        single_list.append(list2[0])
        single_list.append(list2[1])
        single_list.append(float(list2[2]))
        specie_pathway_abun.append(single_list)
    #print(specie_pathway_abun)
    print(len(specie_pathway_abun))
    specie_pathway_abun_file.close()

    pathway_set = set()
    for i in specie_pathway_abun:
        pathway_set.add(i[0])
    print("pathway1 set count:" + str(len(pathway_set)))
    print("get_specie_pathway_abun finished")
    return specie_pathway_abun


def get_speice_compound_weight(specie_pathway_abun, all_pathway_com_path, outfile_path):

    all_path_com_file=open(all_pathway_com_path,'r')
    pathway_compound=[]
    for line in all_path_com_file:
        single_path_com=[]
        line=line.strip()
        lst=line.split('\t')
        single_path_com.append(lst[0])
        single_path_com.append(set(lst[1:]))
        pathway_compound.append(single_path_com)
    #print(pathway_compound)
    all_com_spe_abun = []
    print(len(pathway_compound))
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
    print(len(all_com_spe_abun))

    write_file = open(outfile_path, 'w+')
    for line in all_com_spe_abun:
        string1 = line[0] + '\t' + line[1] + '\t' + str(line[2]) + '\n'
        write_file.write(string1)
    write_file.close()
    print("writing finished")


def main():
    all_pathway_com_path = "/home/zc/IDBdata/all-pathway-compound-filter3.txt"

    pathway_specie_pathabun_path="/home/zc/IDBdata/three-IBD4/ex12/mid-train/path_spe_gui1log.csv"
    specie_pathway_abun = get_specie_pathway_abun(pathway_specie_pathabun_path)
    outfile_path = "/home/zc/IDBdata/three-IBD4/ex12/mid-train/spece_compound_weight.txt"
    get_speice_compound_weight(specie_pathway_abun,all_pathway_com_path , outfile_path)


main()

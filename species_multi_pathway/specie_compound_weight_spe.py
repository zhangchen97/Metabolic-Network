
def get_specie_pathway_abun(specie_abun_path,pathway_specie_pathabun_path):
    specie_abun_file=open(specie_abun_path,'r')
    specie_abun={}
    for line in specie_abun_file:
        line=line.strip()
        list1=line.split("\t")
        specie_abun[list1[0]]=list1[1]
    specie_abun_file.close()

    specie_pathway_abun_file=open(pathway_specie_pathabun_path,'r')
    specie_pathway_abun=[]
    for line in specie_pathway_abun_file:
        line=line.strip()
        single_list=[]
        list2=line.split("\t")
        single_list.append(list2[0])
        single_list.append(list2[1])
        single_list.append(float(list2[2]))
        specie_pathway_abun.append(single_list)
    #print(specie_pathway_abun)
    print(len(specie_pathway_abun))
    specie_pathway_abun_file.close()

    for single_spw in reversed(specie_pathway_abun):
        if single_spw[1] in specie_abun.keys():
            single_spw[2]=float(specie_abun[single_spw[1]])*single_spw[2]*100
        else:
            #print(specie_pathway_abun.index(single_spw))
            del specie_pathway_abun[specie_pathway_abun.index(single_spw)]
    print(specie_pathway_abun)
    print(len(specie_pathway_abun))
    print("get_specie_pathway_abun finished")
    return specie_pathway_abun


def get_speice_compound_weight(specie_pathway_abun,pathway_compound,outfile_path):

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


######################################allnon_specie_abudance_ave.csv#####################
#########################################!!!!!!!!!!!!!!!!!!!!!!!!##########################

def main():
 specie_abun_path="/home/zc/IDBdata/all_data/species-analysis/allibd_specie_abudance_ave.csv"
 all_filter_pathway_compound_path="/home/zc/IDBdata/all-pathway-compound-filter1.txt"

 pathway_specie_pathabun_path="/home/zc/IDBdata/IBD-non-species-compound-static/ibd/path_spe_gui1log.csv"
 specie_pathway_abun=get_specie_pathway_abun(specie_abun_path,pathway_specie_pathabun_path)
 outfile_path="/home/zc/IDBdata/IBD-non-species-compound-static/ibd/spece_compound_weight.txt"
 get_speice_compound_weight(specie_pathway_abun,all_filter_pathway_compound_path,outfile_path)
main()
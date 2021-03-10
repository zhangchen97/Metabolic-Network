from bs4 import BeautifulSoup
import requests
import re
requests.adapters.DEFAULT_RETRIES = 5

def get_reaction(reaction_path):
    reaction_file=open(reaction_path,'r')
    reaction_set=set()
    for line in reaction_file:
        line=line.strip()
        n=0
        l1=line.split('\t')
        if(len(l1)>1):
            for i in l1:
                if(n>0):
                    reaction_set.add(i)
                n=n+1
    reaction_file.close()
    return reaction_set

def craw_compound(reaction_list,compound_path):
    outputfile=open(compound_path,'w+')
    reaction_list=sorted(list(reaction_list))
    print("reaction_list")
    print(reaction_list)
    time=0
    for reaction_id in reaction_list:
        url="https://metacyc.org/META/reaction-genes?object="+reaction_id
        #print(url)
        s = requests.session()
        s.keep_alive = False  # 关闭多余连接
        html_doc = s.get(url).content
        time=time+1
        print(time)
        # 创建一个BeautifulSoup解析对象
        soup = BeautifulSoup(html_doc, "html.parser", from_encoding="utf-8")
        content = soup.text
        list_content=content.split('\n')
        for i in list_content:
            if i=='':
                list_content.remove(i)
        reaction_formula=list_content[1]

        list_compound=[]

        try:
            left_right_compound = re.split(r' -> | <- | <--> ', reaction_formula)
            while "" in left_right_compound:
                left_right_compound.remove("")
            list1=left_right_compound[0].split(" + ")+left_right_compound[1].split(" + ")
            for i in list1:
                list_compound.append(i)
        except IndexError:
                continue

        list_compound1=[]
        for compound1 in list_compound:
                com=compound1.strip()
                match = re.findall(r'^\d |^n ', com)
                match="".join(match)
                com=com.replace(match,"")
                list_compound1.append(com)

        for i in reversed(list_compound1):
            if i=='':
             list_compound1.remove(i)

        line=reaction_id+'\t'+'\t'.join(list_compound1)+'\n'
        outputfile.write(line)

    outputfile.close()
    print("finished")

def main():
    print("ex4 test")
    reaction_path="/home/zc/Downloads/IDBdata/experiment5-non-vali/data-test/reaction_each_pathway.txt"
    compound_path="/home/zc/Downloads/IDBdata/experiment5-non-vali/data-test/compound_each_reaction.txt"
    reaction_list=get_reaction(reaction_path)

    craw_compound(reaction_list,compound_path)
main()
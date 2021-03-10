import re
import requests
from bs4 import BeautifulSoup
def crawler(inputpath,outpath):

    inputfile=open(inputpath,'r')
    outfile = open(outpath, 'w+')
    j=0
    for id in inputfile:
        id=id.strip()
        url="https://metacyc.org/META/pathway-genes?object="+id
        s = requests.session()
        s.keep_alive = False  # 关闭多余连接
        html_doc = s.get(url).content
        j=j+1
        print(j)
        #创建一个BeautifulSoup解析对象
        soup = BeautifulSoup(html_doc,"html.parser",from_encoding="utf-8")
        content=soup.text
        format1=content.split("\n")  #分行
        #print(format1)
        #删除空元素
        for i in format1:
            if i=='':
                format1.remove(i)

        reaction_id=[]
        n = 0
        for line in format1:
            if(n>1):
                try:
                    list_content=line.split("\t")
                    #print(list_content)
                    reaction_id.append(list_content[3])
                except IndexError:
                    pass
                continue

            n=n+1

        line2=id+"\t"+"\t".join(set(reaction_id))+'\n'
        outfile.write(line2)
    inputfile.close()
    outfile.close()
    print("finish")


def main():
    print("ex3 test")
    inpath="/home/zc/Downloads/IDBdata/experiment5-non-vali/data-test/all_pathway_dict.txt"
    #id_list=['PWY-6125','PWY66-422','PWY-6111','PWY-6129']
    outpath="/home/zc/Downloads/IDBdata/experiment5-non-vali/data-test/reaction_each_pathway.txt"
    crawler(inpath,outpath)
main()




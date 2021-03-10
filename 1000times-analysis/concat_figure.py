import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt
file_list=os.listdir("/home/zc/IDBdata/1000times-result/result")
print(file_list)
i=0
for file in file_list:
    path="/home/zc/IDBdata/1000times-result/result/"+file
    #list=open(path,"r")
    #df=pd.Series(list).to_frame()
    df=pd.read_csv(path,header=None,sep="\t")
    if(i==0):
        df_all=df
    else:
        df_all=pd.concat([df_all,df])
    i=i+1
print(df_all.head())
df_all.set_index(0,inplace=True)
print(df_all.shape)
print(df_all.head())
df_all.columns=["non","ibd","ibd&non"]
print(df_all.head())
ibd = df_all['ibd']
non = df_all['non']
ibd_non=df_all['ibd&non']
# 绘制男女乘客年龄的直方图
sns.distplot(ibd, bins = 4, kde = False, hist_kws = {'color':'yellow'}, label = 'ibd')
# 绘制女性年龄的直方图

sns.distplot(non, bins = 4, kde = False, hist_kws = {'color':'green'}, label = 'non')
sns.distplot(ibd_non, bins = 4, kde = False,hist_kws = {'color':'red'}, label = 'ibd&non')
plt.title('the nmi of traing and testing')
plt.ylabel('frequency',fontsize=13)
plt.xlabel('NMI',fontsize=13)
# 显示图例
plt.legend()
# 显示图形
plt.show()

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
# seaborn模块绘制分组的直方图和核密度图
# 读入数据
Titanic = pd.read_csv('/home/zc/IDBdata/y-final-result/nmi1.csv',sep='\t')

ibd = Titanic['ibd']
non = Titanic['non']
ibd_non=Titanic['ibd&non']
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
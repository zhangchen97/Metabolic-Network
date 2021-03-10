from sklearn import metrics
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def NMI_matrix(df):  # 计算标准化互信息矩阵
    number = df.columns.size  # 获取df的列数
    List = []
    Name = []
    for n in range(number):
        Name.append(df.columns[n])  # 获取dataframe的索引
    for i in range(number):
        A = []
        X = df[df.columns[i]]  # df.columns[i]获取对应列的索引，df['索引']获取对应列的数值
        for j in range(number):
            Y = df[df.columns[j]]
            #A.append(metrics.normalized_mutual_info_score(X, Y,average_method='arithmetic'))  # 计算标准化互信息
            A.append(metrics.adjusted_mutual_info_score(X, Y,average_method='arithmetic'))  # 计算AMI
        List.append(A)  # List是列表格式
    print('NMI(标准化互信息) = \n', pd.DataFrame(List, index=Name, columns=Name))  # 将二维列表转为dataframe格式
    figure, ax = plt.subplots(figsize=(12, 12))
    sns.heatmap(pd.DataFrame(List, index=Name, columns=Name), square=True, annot=True, ax=ax)  # 画出热力图
    plt.show()


if __name__ == '__main__':
    path ="/home/zc/PycharmProjects/metabolic/src/analysis/nmi_test.csv"
    #'/home/zc/Downloads/iris-data/Iris.csv'
    data = pd.read_csv(path,header=None)  # 读取csv格式的数据
    print(data)
    df = data.iloc[:, :4]  # 取前四列数据
    NMI_matrix(df)  # df是dataframe格式,计算df的标准化互信息矩阵


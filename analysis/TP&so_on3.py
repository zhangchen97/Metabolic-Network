import pandas as pd
import numpy as np
import seaborn as sns
from sklearn.metrics import confusion_matrix

c_true=[1,1,1,2,2,2,3,3,3]
c_pred=[4,4,4,5,5,5,6,6,7]
#(cluster_id,(index)) ,then groupbykey,
length=len(c_true)
index=list(range(0,length))
pred_arr=list(zip(*[c_pred,index]))
true_arr=list(zip(*[c_true,index]))
print(pred_arr)
print(true_arr)

pred_dict={}
pred_cluster_list=[]
for i in pred_arr:
    pred_dict.setdefault(i[0], set())  # 添加个空set
    pred_dict[i[0]].add(i[1])
    if(i[0] not in pred_cluster_list):
        pred_cluster_list.append(i[0])
pred_cluster_count=len(pred_dict)
print("predict cluster count: "+str(pred_cluster_count))
print(pred_dict)
true_cluster_list=[]
true_dict={}
for i in true_arr:
    true_dict.setdefault(i[0], set())  # 添加个空set
    true_dict[i[0]].add(i[1])
    if(i[0] not in true_cluster_list):
        true_cluster_list.append(i[0])
true_cluster_count=len(true_dict)
print("true cluster count: "+str(true_cluster_count))
print(true_dict)
inter_list=[]
for tru_c,tru_in in true_dict.items():  #{4: {0, 1, 2}, 5: {3, 4, 5}, 6: {6, 7}, 7: {8}}
    for pre_c,pre_in in pred_dict.items():
        inter=tru_in.intersection(pre_in)
        inter_list.append(len(inter))
print(str(len(inter_list))+"="+str(len(true_dict))+" * "+str(len(pred_dict)))
print(inter_list)
print(pred_cluster_list)
for i in range(0,true_cluster_count):
    max_value=max(inter_list)
    if(max_value>0):
        max_index=inter_list.index(max_value)
        change_pred_cluster=int(max_index/pred_cluster_count)
        pred_to_true_clu=max_index%pred_cluster_count
        inter_list[max_index]=0
        print(change_pred_cluster)
        print(pred_to_true_clu)
        pred_dict[true_cluster_list[pred_to_true_clu]]=pred_dict.pop(pred_cluster_list[change_pred_cluster])
print(pred_dict)
print(true_dict)
alterd_pred_list=[0]*len(c_true)
for clu,index in pred_dict.items():
    for i in index:
        alterd_pred_list[i]=clu
print(alterd_pred_list)

cm = confusion_matrix(c_true, alterd_pred_list)
print(cm)
cm = cm.astype(np.float32)
FP = cm.sum(axis=0) - np.diag(cm)
FN = cm.sum(axis=1) - np.diag(cm)
TP = np.diag(cm)
TN = cm.sum() - (FP + FN + TP)
'''
# Sensitivity, hit rate, recall, or true positive rate
TPR = TP / (TP + FN)
# Specificity or true negative rate
TNR = TN / (TN + FP)
# Precision or positive predictive value
PPV = TP / (TP + FP)
# Negative predictive value
NPV = TN / (TN + FN)
# Fall out or false positive rate
FPR = FP / (FP + TN)
# False negative rate
FNR = FN / (TP + FN)
# False discovery rate
FDR = FP / (TP + FP)
'''
# Overall accuracy
ACC = (TP + TN) / (TP + FP + FN + TN)
# ACC_micro = (sum(TP) + sum(TN)) / (sum(TP) + sum(FP) + sum(FN) + sum(TN))
ACC_macro = np.mean(ACC)  # to get a sense of effectiveness of our method on the small classes we computed this average (macro-average)

#F1 = (2 * PPV * TPR) / (PPV + TPR)
#F1_macro = np.mean(F1)
print(ACC)
print(ACC_macro)
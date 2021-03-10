import birankpy as bi
import pandas as pd

inpath="/home/zc/IDBdata/three-non5-22/ex23/mid-train/spe_comp_wei_spark.txt/part-00000"
df=pd.read_csv(inpath,names=['src','dst','weight'],sep='\t')
print(df.src.nunique())
print(df.dst.nunique())
bn=bi.BipartiteNetwork()
bn.set_edgelist(df,top_col='src',bottom_col='dst',weight_col='weight')

hits_birank_df, _ = bn.generate_birank(normalizer='HITS')
hits_res=hits_birank_df.sort_values(by='src_birank', ascending=False).head()
print("HITS")
print(hits_res)
'''
cohits_birank_df, _ = bn.generate_birank(normalizer='CoHITS')
cohits_res=cohits_birank_df.sort_values(by='src_birank', ascending=False).head()
print("CoHITS")
print(cohits_res)

birank_birank_df, _ = bn.generate_birank(normalizer='BiRank')
birank_res=birank_birank_df.sort_values(by='src_birank', ascending=False).head()
print("BiRank")
print(birank_res)
'''
#bgrm_birank_df, _ = bn.generate_birank(normalizer='BGRM')
#bgrm_res=bgrm_birank_df.sort_values(by='src_birank', ascending=False).head()
#print("BGRM")
#print(bgrm_res)
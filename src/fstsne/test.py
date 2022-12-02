import numpy as np
import pandas as pd
import snap

# data = pd.read_csv("/home/myeongwon/mw_dir/FS_TSNE/data/breast_cancer.csv")
# data = data["diagnosis"]

# npy_data = np.load("/home/myeongwon/mw_dir/FS_TSNE/result/breast_cancer/perplexity_15_max_iter_500_learning_rate_200_/breast_cancer_pca_embedded.npy")
# df = pd.DataFrame(npy_data)

# df['2'] = data

# if '2' in df.columns:
#     df = df.drop('2', axis=1)

# data = df.to_numpy()

# print(data.shape)

# g1 = snap.TUNGraph.New()

# for i in range(5):
#     g1.AddNode(i)

# g1.AddEdge(1,2)
# g1.AddEdge(2,3)
# g1.AddEdge(4,3)
# g1.AddEdge(4,0)
# g1.AddEdge(2,0)
# g1.AddEdge(1,0)
# g1.AddEdge(3,2)

# for edge in g1.Edges():
#     print(g1.IsEdge(*(edge.GetId())))
#     #print(edge.GetId())
#     #print(edge.GetId()==(2,3))

# def foo(x):
#     if(x):
#         return False, 1
#     return True, None

# a, b = foo(True)
# c, d = foo(False)
# print(a,b)
# print(c,d)


data = np.array([[1,2], [3,4],[5,6]])

M = (data).shape[0]
dist_matrix = np.zeros((M,M))
temp = np.sum(np.square(data), axis=1)
temp2 = 2*np.matmul(data, data.T)
print(temp.shape)
print(temp2.shape)
dist_matrix = temp + temp.reshape(-1,1) - temp2
print(1)
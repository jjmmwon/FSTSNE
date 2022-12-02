import TSNE
import pandas as pd
import numpy as np

HPram = {"Perplexity" : [10], "Iteration" : [500, 750], "Learning_Rate" : [800, -1]}

hpram = [(p, i, lr) for p in HPram['Perplexity'] for i in HPram['Iteration'] for lr in HPram['Learning_Rate'] ]


file_path = f'/home/myeongwon/mw_dir/FS_TSNE/data/fashion-mnist.csv'

data = pd.read_csv(file_path)
data = data.dropna()

target = data['label'].to_list()
data = data.drop('label', axis=1)
data = data.values

data_name = "F-MNIST"


for p, i, lr in hpram:
    tsne = TSNE.TSNE(data_name=data_name, original_data= data, target=target)

    kwargs = {}
    kwargs['perplexity'] = p
    kwargs['max_iter'] = i
    if lr == -1:
        kwargs['learning_rate'] = "auto"
    else:
        kwargs['learning_rate'] = lr

    tsne.run( random_iter = 10, pca_iter= 1, **kwargs)

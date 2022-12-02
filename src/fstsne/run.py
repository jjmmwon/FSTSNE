from tqdm import tqdm
import TSNE
import pandas as pd
import numpy as np

# data_list = [('breast_cancer.csv','diagnosis'),('milknew.csv','Grade'),('mobile_price.csv','price_range'),('black_politicians.csv',''),
# ('injury.csv',''),('fashion-mnist.csv','label'),('mm_nhis.csv',''),('diabetes.csv','Diabetes_012'),('labsup.csv','')]

data_list = [("Dry_Bean_Dataset.xlsx", ""), ("Cigar.csv", ""), ("BudgetItaly.csv", ""), ("BudgetUK.csv", ""),
            ("Frogs_MFCCs.csv", "")]


HPram = {"Perplexity" : [15, 30, 45], "Iteration" : [500, 750, 1000], "Learning_Rate" : [200, 800, -1]}

hpram = [(p, i, lr) for p in HPram['Perplexity'] for i in HPram['Iteration'] for lr in HPram['Learning_Rate'] ]


for d, c in data_list:
    file_path = f'/home/myeongwon/mw_dir/FS_TSNE/data/{d}'
    if 'csv' in d:
        data = pd.read_csv(file_path)
    if 'xls' in d:
        data = pd.read_excel(file_path)

    data = data.dropna()

    data_dict = dict(data.dtypes)
    for k, v in data_dict.items():
        if c != '' and k == c:
            continue
        if v == np.object0:
            data = data.drop(k, axis=1)
        if "Unnamed" in k:
            data = data.drop(k, axis=1)

    if c != '':
        target = data[c].to_list()
        data = data.drop(c, axis=1)
    else:
        target = None

    data = data.values

    data_name = d[:-4]
    print(data_name)

    for p, i, lr in tqdm(hpram):
        tsne = TSNE.TSNE(data_name=data_name, original_data= data, target=target)

        kwargs = {}
        kwargs['perplexity'] = p
        kwargs['max_iter'] = i
        if lr == -1:
            kwargs['learning_rate'] = "auto"
        else:
            kwargs['learning_rate'] = lr

        tsne.run( random_iter = 10, pca_iter= 1, **kwargs)

# fn = args.file_name[:-4]
# print(fn)

# cmd = f'python3 GraphGen.py -d {fn}'
# subprocess.run([cmd], shell=True, check=True)

# cmd = f'python3 FSM.py -d {fn}'
# subprocess.run([cmd], shell=True, check=True)
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm

import os
from sklearn.preprocessing import MinMaxScaler
import argparse
import json

import sys
sys.path.append('/home/myeongwon/mw_dir/t-sneEvaluation/fitsne')
sys.path.append('/home/myeongwon/mw_dir/t-sneEvaluation/snc')

from fast_tsne import fast_tsne
from snc import SNC

class TSNE:
    def __init__(self, data_name, original_data, target = None):
        self.data_name = data_name
        self.original_data = original_data
        self.target = target

        self.instances, self.attributes = original_data.shape

        self.save_path = None
        self.kwargs = {}
        self.embedded_data = None
        self.path = None

        self.init = None

        self.loss = {'pca':[], 'random':[]}
        self.SnC = {'pca':[], 'random':[]}

    def fit(self, init = 'random', return_loss = True, **kwargs):
        """
        Applying FIt-SNE to original data

        """
        self.kwargs = kwargs
        self.init = init
        X = self.original_data
        X = MinMaxScaler().fit_transform(X)

        Z = fast_tsne(X, initialization = init, return_loss = return_loss, **kwargs)

        if return_loss :
            self.embedded_data , loss = Z            
            self.loss[self.init].append(loss[-1])

        else:
            self.embedded_data = Z

        self.save_path = f'{self.data_name}_{ self.init }'
        

    def save_embedded_data(self, save_plot = False):
        """
        save embedded data
        """

        path = f'/home/myeongwon/mw_dir/FS_TSNE/result/{self.data_name}'
        if not os.path.isdir(path):
            os.mkdir(path)
        path = path + '/'

        for k, v in self.kwargs.items():
            path = path + f'{k}_{v}_'
        if self.kwargs == {}:
            path = path + 'Default'
        
        self.path = path

        if not os.path.isdir(self.path):
            os.mkdir(self.path)


        # if save_plot:
        #     self.plot()
        save_data = pd.DataFrame(self.embedded_data)
        if self.target:
            df = pd.DataFrame(self.target)
            save_data['2'] = df

        if os.path.isfile(f'{path}/{self.save_path}_embedded.csv'):
            i = 1
            while(os.path.isfile(f'{path}/{self.save_path}_embedded{i}.csv')):
                i = i+1
            save_data.to_csv(f'{path}/{self.save_path}_embedded{i}.csv')
        else:
            save_data.to_csv(f'{path}/{self.save_path}_embedded.csv')

    def plot(self):
        """
        save the plot of embedded data
        """
        
        plt.figure(figsize=(6,6))
        plt.axis('equal')
        plt.scatter(self.embedded_data[:,0], self.embedded_data[:,1], s = 2, c=self.target, cmap= plt.cm.tab20, alpha=0.6)
        plt.tight_layout()

        path = self.path
        if os.path.isfile(f'{path}/{self.save_path}.png'):
            i = 1
            while(os.path.isfile(f'{path}/{self.save_path}{i}.png')):
                i = i+1
            plt.savefig(f'{path}/{self.save_path}{i}.png')
        else:
            plt.savefig(f'{path}/{self.save_path}.png')
        #plt.show()

    def measure(self):
        """
        Measuring an embedded data with SNC method
        """
        metrics = SNC( raw = self.original_data, emb = self.embedded_data, iteration=300)
        metrics.fit()

        snc = (metrics.steadiness(), metrics.cohesiveness())

        self.SnC[self.init].append(snc)

    def save_result(self):
        #path = f'/home/myeongwon/mw/tsne/result/{self.data_name}'
        #if not os.path.isdir(path):
        #    os.mkdir(path)

        result = {'Shape' : {'Instances': self.instances, "Attributes" : self.attributes}}

        if self.kwargs == {}:
            result['Hyperparameter'] = "Default"
        else:
            result['Hyperparameter'] = self.kwargs

        result['pca'] = []
        result['random'] = []

        for l, (s, c) in zip(self.loss['pca'], self.SnC['pca']):
            result['pca'].append({
                "Loss" : l,
                "Steadiness" : s,
                "Cohesiveness" : c
            })

        for l, (s, c) in zip(self.loss['random'], self.SnC['random']):
            result['random'].append({
                "Loss" : l,
                "Steadiness" : s,
                "Cohesiveness" : c
            })

        path = f'/home/myeongwon/mw_dir/FS_TSNE/result/{self.data_name}'
        file_path = f'{path}/{self.data_name}_result.json'

        """
        Save the result format as
        [{shape : {}, Hyperparameter : {}, pca : [], rand : []}, {shape : {}, Hyperparameter : {}, pca : [], rand : []}, ... ]
        """
        if os.path.isfile(file_path):
            with open(file_path, "r") as json_file:
                json_data = json.load(json_file)

            json_data.append(result)

            with open(file_path, "w") as json_file:
                json.dump(json_data, json_file, indent="\t")
        else:
            json_data = [result]
            with open(file_path, "w") as json_file:
                json.dump(json_data, json_file, indent="\t")

    def run(self, pca_iter = 1, random_iter = 10, save_plot = False, **kwargs):

        for _ in tqdm(range(pca_iter), desc="PCA Iteration"):
            self.fit(init='pca', return_loss = True, **kwargs)
            print("""
            Measuring S&C
            """)
            self.measure()
            self.save_embedded_data(save_plot)

        for _ in tqdm(range(random_iter), desc="Random Iteration"):
            self.fit(init = 'random', return_loss = True, **kwargs)
            print("""
            Measuring S&C
            """)
            self.measure()
            self.save_embedded_data(save_plot)

        
        self.save_result()



def argparsing():
    parser = argparse.ArgumentParser(description="Dimension Reduction using t-SNE and Evaluation")
    parser.add_argument('--file_path', '-f', help="File path to use for Dimension Reduction and Evaluation")
    parser.add_argument('--pca_iter','-p', type= int, default= 1, help='Number of iteration to PCA initalization' )
    parser.add_argument('--random_iter','-r', type= int, default= 10, help='Number of iteration to random initalization' )
    #parser.add_argument('--plot', '-P', action = 'store_true', default   = False, help="Plot embedded data")
    parser.add_argument('--perplexity', '-P', type = int, action = 'store', default = 30, help="Perplexity used for fit-sne")
    parser.add_argument('--max_iter', '-I', type = int, action = 'store', default = 750, help="Iteration used for fit-sne")
    parser.add_argument('--learning_rate', '-L', type = int, action = 'store', default = -1, help="Learning Rate used for fit-sne")
    parser.add_argument('--class_col','-C', default= None, help="Name of column wanted to classify" )

    args = parser.parse_args()

    return args

def main():
    args = argparsing()

    if 'csv' in args.file_path:
        data = pd.read_csv(args.file_path)
    if 'xls' in args.file_path:
        data = pd.read_excel(args.file_path)

    data = data.dropna()

    data_dict = dict(data.dtypes)
    for k, v in data_dict.items():
        if args.class_col and k == args.class_col:
            continue
        if v == np.object0:
            data = data.drop(k, axis=1)
        if "Unnamed" in k:
            data = data.drop(k, axis=1)

    if args.class_col:
        target = data[args.class_col].to_list()
        data = data.drop(args.class_col, axis=1)
    else:
        target = None

    data = data.values

    idx = [i for i, c in enumerate(args.file_path) if c == '/']
    file_name = args.file_path[idx[-1]+1:-4]

    tsne = TSNE(data_name=file_name, original_data= data, target=target)

    kwargs = {}
    kwargs['perplexity'] = args.perplexity
    kwargs['max_iter'] = args.max_iter
    if args.learning_rate == -1:
        kwargs['learning_rate'] = "auto"
    else:
        kwargs['learning_rate'] = args.learning_rate

    tsne.run( random_iter = args.random_iter, pca_iter= args.pca_iter, **kwargs)

if __name__ == '__main__':
    main()












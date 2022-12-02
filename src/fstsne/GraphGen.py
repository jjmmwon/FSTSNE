import glob
import os
import numpy as np
import pandas as pd
import snap
import argparse
from tqdm import tqdm

class GraphGenerator:
    def __init__(self, data_title, k=5):
        self.data_title = data_title
        self.path = f'/home/myeongwon/mw_dir/FS_TSNE/result/{data_title}/'
        self.k = k
        self.graph = None
        self.current_file = None
        self.dist_matrix = None


    def distant_matrix(self, data): # generate distant matrix 
        M = data.shape[0]
        print(data[8], data[15])
        self.dist_matrix = np.zeros((M,M))
        self.dist_matrix = np.sum(np.square(data), axis=1) + (np.sum(np.square(data), axis=1)).reshape(-1,1) - 2*np.matmul(data, data.T)


    def make_graph(self):   # make graph with k neighbors per each point
        self.graph = snap.TUNGraph.New()
        for i in range(self.dist_matrix.shape[0]):
            self.graph.AddNode(i)
        idx = 0
        for row in self.dist_matrix:
            nearest_neighbor = row.argsort()
            if idx == 8:
                print(idx, row[15], nearest_neighbor[:20])

            for i in range(1,self.k+1):
                self.graph.AddEdge(int(idx), int(nearest_neighbor[i]))
            idx += 1
        

    def save_graph(self):   # save graph file using snap lib
        save_path = self.current_file[:-4]

        FOut = snap.TFOut(f'{save_path}_k_{self.k}.graph')
        self.graph.Save(FOut)
        FOut.Flush()


    def save_graphViz(self):
        dir_path = self.path + 'graphViz'
        if not os.path.isdir(dir_path):
            os.mkdir(dir_path)
        graph_title = self.current_file[len(self.path):-4]

        labels = {}
        for NI in self.graph.Nodes():
            labels[NI.GetId()] = str(NI.GetId())
        self.graph.DrawGViz(snap.gvlDot, f'{dir_path}/{graph_title}.png', " ", labels)



    def run(self):
        path = self.path + '/*/*.csv'
        
        csv_files = glob.glob(path)
        #print(len(csv_files))
        
        for csv_file in tqdm(csv_files):
            self.current_file = csv_file
            data = pd.read_csv(self.current_file)
                        
            if '2' in data.columns:
                data = data.drop('2', axis=1)

            data = data.to_numpy()
            data = data[:, 1:]
            print(data.shape)
            print("Generating distance_matrix")
            self.distant_matrix(data)
            print("Generating graph")
            self.make_graph()
            print("Saving graph")
            self.save_graph()
            #self.save_graphViz()
        

def argparsing():
    parser = argparse.ArgumentParser(description="Make kNN Graph from MDP data")
    parser.add_argument('--data', '-d', help="MDP data for making graph")
    parser.add_argument('--neighbors', '-k', type = int, action = 'store', default = 5, help="Number of neighbor for graph")

    args = parser.parse_args()
    return args

def main():
    args = argparsing()
    print("Data: "+args.data, "\nNeighbors: "+ str(args.neighbors))

    gmaker = GraphGenerator(args.data, args.neighbors)
    gmaker.run()

if __name__== "__main__":
    main()

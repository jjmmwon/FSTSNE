import os
import glob
import json
import argparse

import snap
import numpy as np
from tqdm import tqdm

class FSM:
    def __init__(self, graph_title, path, min_support=8):
        self.graph_title = graph_title
        self.min_support = min_support

        self.path = path 
        self.graph_set = []
        self.mother_graph = None
        
        self.FS_set = []
        self.data_len = None
        self.node_len = None
        self.adjList = None
        

    def load_graphs(self):
        # graph를 snap.py에서 제공하는 graph 형식으로 load
        graph_path = self.path + '/*.graph'
        graph_files = glob.glob(graph_path)
        graph_files.sort()
        for graph_file in graph_files:
            FIn = snap.TFIn(graph_file)
            graph = snap.TUNGraph.Load(FIn)
            self.graph_set.append(graph)

        self.data_len = len(graph_files)
        self.node_len = self.graph_set[0].GetNodes()    # 그래프 노드 개수

    def mother_graph_generate(self):
        """
        graph의 모든 edge를 포함하는 mother graph 생성
        """
        self.mother_graph = snap.TUNGraph.New()
        for i in range(self.node_len):
            self.mother_graph.AddNode(i)

        for graph in self.graph_set:
            for edge in graph.Edges():
                self.mother_graph.AddEdge(edge.GetSrcNId(),edge.GetDstNId())

    def frequent_edge(self):
        """
        mother_graph의 모든 edge를 반복하며 min_support 이상 나타나는 edge만 남겨둔다.
        """
        del_edges = []
        for edge in self.mother_graph.Edges():
            count = 11
            for graph in self.graph_set:
                if(not graph.IsEdge(*(edge.GetId()))):
                    count -= 1
                if(count<self.min_support):
                    del_edges.append(edge.GetId())
                    break

        for del_edge in del_edges:
            self.mother_graph.DelEdge(*del_edge)
    
    def adjList_gen(self):
        """
        mother_graph의 adjacency list 생성
        """
        self.adjList = [[] for _ in range(self.node_len)]
        for edge in self.mother_graph.Edges():
            self.adjList[edge.GetSrcNId()].append(edge.GetDstNId())
            self.adjList[edge.GetDstNId()].append(edge.GetSrcNId())

    def get_subgraph(self):
        """
        frequent edge 정보를 통해 frequent subgraph 나눈다.
        node 반복
            visit == true -> 다음노드
            else
                node의 이웃 subgraph에 포함
                subgraph 안의 node 돌면서 이웃 계속 추가
                모두 visit true일 시 sugraph의 node set을 list로 변경시켜 FS_set에 추가
        """
        visit = [False for _ in range(self.node_len)] 
        
        for node in range(self.node_len):
            if visit[node]:
                continue
            visit[node] = True
            subgraph = set([node])
            subgraph.update(self.adjList[node])
            while(True):
                all_visited, next_node = self.isAll_visited(visit, subgraph)

                if all_visited:
                    break
                subgraph.update(self.adjList[next_node])

            subgraph = (list(subgraph))
            if len(subgraph) <=5:
                continue
            self.FS_set.append(subgraph)

    def isAll_visited(self, visit, node_set):
        for node in node_set:
            if not visit[node]:
                visit[node] = True
                return False, node
        return True, None




    # def candidate_gen(self):
    #     if not self.prev_candidate:
    #         for n, v in enumerate(self.visit):
    #             """
                
    #             """


    #             pass

    #     # while False in self.visit:
    #     #     if not self.candidate:
    #     #         for v in range(len(self.visit)-1, -1, -1):
    #     #             if not self.visit[v]:
    #     #                 self.candidate = [v]
    #     #                 self.visit[v] = True
    #     #                 break
    #     #         # for i, n in enumerate(self.visit):
    #     #         #     if not n:
    #     #         #         self.candidate = [i]
    #     #         #         self.visit[i] = True
    #     #         #         break

    #     #     for node in self.candidate:
    #     #         for adj_list in self.adjList_set:
    #     #             for adj_node in adj_list[node]:
    #     #                 if  not self.visit[adj_node]:
    #     #                     self.candidate.insert(0,adj_node)
    #     #                     self.visit[adj_node] = True
    #     #                     return False    # candidate가 생성되면 return
            
    #     #     if self.prev_candidate:  # 방문하지 않은 인접한 node가 없으면 이전 frequent subgraph 저장
    #     #         self.FS_set.append(self.prev_candidate)
    #     #         self.prev_candidate = []

    #     #     self.candidate = [] # 후보 초기화
    #     # return True # 더이상 candidate가 없으면 True return
        
    # def adjList_gen(self):
    #     # Adjacency List 생성
    #     for g in self.graph_set:
    #         adjList = [[] for _ in range(self.node_len)]
    #         for edge in g.Edges():
    #             adjList[edge.GetSrcNId()].append(edge.GetDstNId())
    #             adjList[edge.GetDstNId()].append(edge.GetSrcNId())
    #         self.adjList_set.append(adjList)

    # def subgraph_isomorphism(self, sub_g): 
    #     occurrence_cnt = self.data_len

    #     # ex) subgraph의 edge가 (3,4)인 경우 검색하는 graph의 CAM에서 3번째 $에서 5번쨰 떨어진 값이 1이면 그 graph에 edge가 존재한다는 것을 알 수 있다.
    #     for edge in sub_g.Edges():
    #         if edge.GetSrcNId() < edge.GetDstNId(): 
    #             for cam in self.CAM_set:
    #                 if cam[idx_list[edge.GetDstNId()-1]+edge.GetSrcNId()+1] != "1":
    #                     occurrence_cnt -= 1
    #                     if occurrence_cnt < self.min_support:
    #                         return False
    #         else:
    #             for cam in self.CAM_set:
    #                 if cam[idx_list[edge.GetSrcNId()-1]+edge.GetDstNId()+1] != "1":
    #                     occurrence_cnt -= 1
    #                     if occurrence_cnt < self.min_support:
    #                         return False
    #     return True

    # def is_graph(self, sub_g):
    #     # sub_g로 생성된 것이 그래프인지 확인한다. node에 연결된 edge가 없으면 graph가 아닌 것으로 판단한다.
    #     for node in sub_g.Nodes():
    #         if node.GetOutDeg() == 0:
    #             return False
    #     return True

    def save_FS(self):
        # Frequent subgraph 저장
        json_out = {}        
            
        json_out["Data"] = self.graph_title
        json_out["Neighbor"] = 5
        json_out["Min_support"] = self.min_support
        json_out["FSM"] = self.FS_set

        json_path = self.path + f'/{self.graph_title}_FSM.json'
        # with open(json_path, 'w') as outfile:
        #     json.dump(json_out, outfile)

        if os.path.isfile(json_path):
            with open(json_path, "r") as json_file:
                json_data = json.load(json_file)

            json_data.append(json_out)

            with open(json_path, "w") as json_file:
                json.dump(json_data, json_file, indent="\t")
        else:
            json_data = [json_out]
            with open(json_path, "w") as json_file:
                json.dump(json_data, json_file, indent="\t")


    def run(self):
        self.load_graphs()
        self.mother_graph_generate()        
        self.frequent_edge()
        self.adjList_gen()
        self.get_subgraph()
        self.save_FS()

def argparsing():
    parser = argparse.ArgumentParser(description="Frequent Subgraph Mining")
    parser.add_argument('--data_title', '-d', help="graph data title for FSM")
    parser.add_argument('--min_support', '-s', type = int, action = 'store', default = 8, help="min_support for FSM")

    args = parser.parse_args()
    return args


def main():
    args = argparsing()
    data_path = f'/home/myeongwon/mw_dir/FS_TSNE/result/{args.data_title}/*'
    data_dirs = glob.glob(data_path)
    print(data_dirs)
    print(len(data_dirs))

    for path in tqdm(data_dirs):
        if '.' in path:
            continue
        print(path)
        fsm = FSM(args.data_title, path, args.min_support)
        fsm.run()

if __name__== "__main__":
    main()


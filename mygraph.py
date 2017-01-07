
from graph_tool.all import *
from itertools import izip
from numpy.random import randint
import numpy as np
import scipy.sparse as ssp
import os, subprocess

path="./frames"
if not os.path.exists(path):
    os.makedirs(path)

#random walk Simulation:

#loading graph
h=collection.data["karate"]
vprop_stat=h.new_vertex_property("double")
N=len(list(h.vertices() ))
pos = sfdp_layout(h)

if not os.path.exists(path+"/randomwalk"):
    os.makedirs(path+"/randomwalk")


L=200 # length of random walk

#definig vertex properties for animation purpose. This will help to change color, size, etc. during run of algortithms

vprop_color = h.new_vertex_property("string") 
vprop_blinker= h.new_vertex_property("short") 
vprop_label = h.new_vertex_property("short")

eprop_color = h.new_edge_property("string") 

#ininital node for random walk is chosen to be state 0
state=h.vertex(0)
for i in range(N):
        vprop_color[i]="red"
        vprop_blinker[i]=5
        vprop_label[i]=i
h.vertex_properties["label"] = vprop_label

for e in h.edges():
    eprop_color[e]="black"

for i in range(L):
    prev=state
    state=np.random.choice(list(state.out_neighbours()) ,1)[0]
    vprop_color[state]="blue"
    vprop_blinker[state]=20
    e=h.edge(prev,state)
    eprop_color[e]="blue"
    graph_draw(h, pos, output_size=(1000, 1000), vertex_fill_color= vprop_color, edge_color= eprop_color, vertex_text= h.vertex_index, vertex_size=vprop_blinker, edge_pen_width=2,output="./frames/randomwalk/walk_karate"+str(i)+".svg")
    vprop_color[state]="red"
    vprop_blinker[state]=5
    eprop_color[e]="black"




#============================================================================================================
#BF Search
if not os.path.exists(path+"/bfs"):
    os.makedirs(path+"/bfs")
for i in range(N):
        vprop_color[i]="red"
        vprop_blinker[i]=10

class VisitorExample(BFSVisitor):
    count=0
    def __init__(self, name, pred, dist):
        self.name = name
        self.pred = pred
        self.dist = dist

    def discover_vertex(self, u):
        print("-->", self.name[u], "has been discovered!")
        vprop_color[u]="green"
        vprop_blinker[u]=30
        graph_draw(h, pos, output_size=(1000, 1000), vertex_fill_color= vprop_color, edge_color= eprop_color, vertex_text= h.vertex_index, vertex_size=vprop_blinker, edge_pen_width=2,output="./frames/bfs/bfs_karate"+str(VisitorExample.count)+".svg")
        VisitorExample.count=VisitorExample.count+1

        

    def finish_vertex(self,u):
        vprop_color[u]="blue"
        vprop_blinker[u]=60
        graph_draw(h, pos, output_size=(1000, 1000), vertex_fill_color= vprop_color, edge_color= eprop_color, vertex_text= h.vertex_index, vertex_size=vprop_blinker, edge_pen_width=2,output="./frames/bfs/bfs_karate"+str(VisitorExample.count)+".svg")
        VisitorExample.count=VisitorExample.count+1

    def tree_edge(self, e):
        self.pred[e.target()] = int(e.source())
        self.dist[e.target()] = self.dist[e.source()] + 1

name = h.vp["label"]
dist = h.new_vertex_property("int")
pred = h.new_vertex_property("int64_t")
bfs_search(h, h.vertex(0), VisitorExample(name, pred, dist))

#============================================================================================================
#DF Search
if not os.path.exists(path+"/dfs"):
    os.makedirs(path+"/dfs")

for i in range(N):
        vprop_color[i]="red"
        vprop_blinker[i]=10
class DFSVisitorExample(DFSVisitor):
    count=0
    def __init__(self, name, pred, time):
        self.name = name
        self.pred = pred
        self.time = time
        self.last_time = 0

    def discover_vertex(self, u):
        #print("-->", self.name[u], "has been discovered!")
        self.time[u] = self.last_time
        self.last_time += 1
        vprop_color[u]="green"
        vprop_blinker[u]=30
        graph_draw(h, pos, output_size=(1000, 1000), vertex_fill_color= vprop_color, edge_color= eprop_color, vertex_text= h.vertex_index, vertex_size=vprop_blinker, edge_pen_width=2,output="./frames/dfs/dfs_karate"+str(DFSVisitorExample.count)+".svg")
        DFSVisitorExample.count=DFSVisitorExample.count+1

    def finish_vertex(self,u):
        #print("-->", self.name[u], "has been finished!")
        vprop_color[u]="blue"
        vprop_blinker[u]=60
        graph_draw(h, pos, output_size=(1000, 1000), vertex_fill_color= vprop_color, edge_color= eprop_color, vertex_text= h.vertex_index, vertex_size=vprop_blinker, edge_pen_width=2,output="./frames/dfs/dfs_karate"+str(DFSVisitorExample.count)+".svg")
        DFSVisitorExample.count=DFSVisitorExample.count+1

name = h.vp["label"]
time = h.new_vertex_property("int")
pred = h.new_vertex_property("int64_t")
dfs_search(h, h.vertex(0), DFSVisitorExample(name, pred, time))


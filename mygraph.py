
from graph_tool.all import *
from itertools import izip
from numpy.random import randint
import numpy as np
import scipy.sparse as ssp
import os, subprocess


# g=Graph(directed=False)
# n=10
# g.add_vertex(n)

# # insert some random links
# m=20
# for s,t in izip(randint(0, n, m), randint(0, n, m)):
# 	if s!=t:
# 		g.add_edge(g.vertex(s), g.vertex(t))

# for e in g.edges():
# 	pass
# 	#print e, e.source(), e.target()

# vprop_label = g.new_vertex_property("short")
# vprop_color = g.new_vertex_property("string") 

# for v in g.vertices():
# 	vprop_label[v]=randint(0,10,1)
# 	if vprop_label[v]%2==0:
# 		vprop_color[v]="red"
# 	else:
# 		vprop_color[v]="blue"

# g.vertex_properties["label"] = vprop_label
# g.vertex_properties["color"] = vprop_color

# pos = sfdp_layout(g)
#graph_draw(g, pos, output_size=(100, 100), vertex_color=[1,1,1,0], vertex_fill_color=g.vertex_properties["color"] , vertex_size=2, edge_pen_width=0.05,output="graph.pdf")
#======================================================================================================
path="./frames"
if not os.path.exists(path):
    os.makedirs(path)

g=collection.data["karate"]
A=transition(g)
vprop_stat=g.new_vertex_property("double")
N=len(list(g.vertices() ))

pos = graph_tool.draw.sfdp_layout(g)
graph_draw(g, pos, output_size=(1000, 1000), vertex_color=[1,1,1,0], vertex_fill_color="red" , vertex_size=1, edge_pen_width=0.3,output="karate.png")
#=================================================
#pagerank

if not os.path.exists(path+"/pagerank"):
    os.makedirs(path+"/pagerank")

v=ssp.lil_matrix((N, 1))
damp=ssp.lil_matrix((N,1))
for i in range(N):
    v[i,0]=1/float(N)
    damp[i,0]=1/float(N)
    vprop_stat[i]=600/float(N)

graph_draw(g, pos, output_size=(1000, 1000), vertex_fill_color="green" , vertex_size=vprop_stat, edge_pen_width=0.3,output=path+"/pagerank/"+"page"+str(0)+".svg")
LL=20
for j in range(1,LL):
    v=0.85*A*v+0.15*damp
    for i in range(N):
        vprop_stat[i]=v[i,0]*600
        graph_draw(g, pos, output_size=(1000, 1000), vertex_fill_color="green"  , vertex_size=vprop_stat, edge_pen_width=0.3,output=path+"/pagerank/"+"page"+str(j)+".svg")


#======================================================================================================================================
#random walk 
h=collection.data["karate"]
A=transition(h)
vprop_stat=h.new_vertex_property("double")
N=len(list(h.vertices() ))
pos = sfdp_layout(h)

if not os.path.exists(path+"/randomwalk"):
    os.makedirs(path+"/randomwalk")


L=200 # length of random walk
vprop_color = h.new_vertex_property("string") 
vprop_blinker= h.new_vertex_property("short") 
vprop_label = h.new_vertex_property("short")

eprop_color = h.new_edge_property("string") 

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


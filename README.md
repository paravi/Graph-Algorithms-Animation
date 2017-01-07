# Graph-Algorithms-Animation
This repo is an simple illustration for graph search/exploration algorithms using python. This involves Breadth-first searach, Depth-first search and a random walk simulation. The purpose of animations is to illustrate how these algorithms work in principle.

## Dependencies
The script is written is python and is based on graph-tools package:

Tiago P. Peixoto, “The graph-tool python library”, figshare. (2014) DOI: 10.6084/m9.figshare.1164194


## Example Run
python mygraph.py

A series of images correspondig to algorithm runs will be created in the folder ./frames and specific figures are saved in subfolders such as ./frames/dfs or ./frames/bfs , etc. In current code, the animations are created for existing network called Karate Club in graph-tools module.

For creating animation, one can use 'convert' command in shell, which is listed in ./createanim.sh:

chmod +x createanim.sh

./createanim.sh

## Demos
Demos are saved in ./bfs.gif, ./dfs.gif, etc.

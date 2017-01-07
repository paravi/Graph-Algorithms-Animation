convert $(for ((a=0; a<20; a++)); do printf -- "-delay 50 ./frames/pagerank/page%s.svg " $a; done;) PageRankAnimation.gif
convert $(for ((a=0; a<200; a++)); do printf -- "-delay 50 ./frames/randomwalk/walk_karate%s.svg " $a; done;) RandomWalk.gif
convert $(for ((a=0; a<68; a++)); do printf -- "-delay 50 ./frames/bfs/bfs_karate%s.svg " $a; done;) bsf.gif
convert $(for ((a=0; a<68; a++)); do printf -- "-delay 50 ./frames/dfs/dfs_karate%s.svg " $a; done;) dfs.gif
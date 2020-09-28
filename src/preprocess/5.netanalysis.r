source("http://Bioconductor.org/biocLite.R")
#biocLite("igraph")
library(igraph)
library(ggplot2)
dictionary = "/Users/jiaminsun/expsjm/bio/data/GBM_three_groups/Ast_NPC/result"
setwd(dictionary)
# read table
gene_npc_nsc1 = read.table("analysis_minus_net.txt",header = T)
g_npc_nsc1 = data.frame(id1=gene_npc_nsc1$Id1,id2=gene_npc_nsc1$Id2)
g = graph_from_data_frame(g_npc_nsc1, directed=FALSE) 
V(g)$size=10
plot(g)
# sorted by g
degree_g=sort(degree(g),decreasing=T)
closeness_g=sort(closeness(g),decreasing=T)
betweenness_g=sort(betweenness(g),decreasing=T)
vector_g=sort(evcent(g,scale = F)$vector,decreasing=T)
# max of four standards
degree_nor=degree(g,normalized = T)
max_d=max(degree_g)
max_c=max(closeness_g)
max_b=max(betweenness_g)
max_v=max(vector_g)
for(i in 1:length(degree_g)){
  degree_g[i]=degree_g[i]/max_d
}
for(i in 1:length(closeness_g)){
  closeness_g[i]=closeness_g[i]/max_c
}
for(i in 1:length(betweenness_g)){
  betweenness_g[i]=betweenness_g[i]/max_b
}
for(i in 1:length(vector_g)){
  vector_g[i]=vector_g[i]/max_v
}
#四个中心度计算 DC CC BC 和特征向量中心度
write.table(degree_g,quote=FALSE,col.names = FALSE,'GBM_degree.txt')
write.table(closeness_g,quote=FALSE,col.names = FALSE,'GBM_closeness.txt')
write.table(betweenness_g,quote=FALSE,col.names = FALSE,'GBM_betweenness.txt')
write.table(vector_g,quote=FALSE,col.names = FALSE,'GBM_vector.txt')

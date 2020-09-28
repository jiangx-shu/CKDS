dictionary = "/Users/jiaminsun/expsjm/single cell"
setwd(dictionary)
library(igraph)
#source("http://Bioconductor.org/biocLite.R")
# biocLite("bc3net")
library(bc3net)
# destination = "new_network"
# filename = "shortlong"
# AD_data = read.csv(paste(filename,"AD_control.csv",sep = "/"),row.names = 1,check.names = F)
# TPM_data = read.csv("GSE104687_TBT_normalized_FPKM.csv",row.names = 1,check.names = F)
# anno = read.csv("anno.csv",row.names = 1,check.names = F)
# 
# object = "TCx"

#sjm  一段有用的代码
#construct network of normal cells*****/
# fwm_gene = read.table("gene-shortlong.txt")
# TPM_data = read.csv("ESET3.csv",row.names = 1,check.names = F)
# index = match(fwm_gene[,1],rownames(TPM_data))
# select_gene = TPM_data[index,]
# write.csv(select_gene, 'Expression_eset3_all.csv', row.names = T, quote = F)
#normal <- as.matrix(read.csv('Expression3.csv', sep=",",header=FALSE))


######start
normal <- as.matrix(read.csv('E_intermediate.csv', sep=",",header=FALSE))
normal_genes <- as.matrix(read.csv('gene-shortlong.csv', sep=",",header=FALSE))
rownames(normal) = normal_genes

normal_net <- bc3net(normal, boot=100, estimator="pearson")
#plot(normal_net)
plot(normal_net, vertex.size=1, vertex.label=NA, edge.arrow.size=0)

#Degree distribution of the network
plot(degree.distribution(normal_net), xlab="Node Degree")
#network density
graph.density(normal_net)
write.graph(normal_net,"netintermediate.txt",format="ncol")

######end



  
#读经过blast匹配筛选后的基因
fwm_gene = read.table(paste(filename,paste(destination,"tcx_93.txt",sep = "/"),sep = "/"))
index = match(fwm_gene[,1],rownames(TPM_data))
select_gene = TPM_data[index,]

isAD = anno$dsm_iv_clinical_diagnosis == "Alzheimer's Disease Type"
isControl = anno$dsm_iv_clinical_diagnosis == "No Dementia"
isFWM = anno$structure_ac == object
disease_data = select_gene[,isAD & isFWM]
normal_data = select_gene[,isControl & isFWM]

disease_data = as.matrix(disease_data)
normal_data = as.matrix(normal_data)
disease_net = bc3net(disease_data,estimator = "spearman")
normal_net = bc3net(normal_data,estimator = "spearman")
tt = V(disease_net)

ff = as_ids(tt)
edge = get.edgelist(disease_net)
index = match(ff,edge)
table(is.na(index))

kk = V(disease_net)
hh = as_ids(kk)
edge1 = get.edgelist(normal_net)
index = match(hh,edge1)
table(is.na(index))

ff = as.data.frame(ff)
ff$value = c(0:(nrow(ff)-1))
edge_disease = get.edgelist(disease_net)

for (i in 1:nrow(edge_disease))
    for (j in 1:ncol(edge_disease))
    {
        n = match(edge_disease[i,j],ff$ff)
        edge_disease[i,j] = ff$value[n]
    }


edge_normal = get.edgelist(normal_net)

for (i in 1:nrow(edge_normal))
    for (j in 1:ncol(edge_normal))
    {
        n = match(edge_normal[i,j],ff$ff)
        edge_normal[i,j] = ff$value[n]
    }
length(tt)
nrow(edge_disease)
nrow(edge_normal)

ff = ff[-93,]
#判断是否少了节点
index = match(ff$value,edge_disease)
table(is.na(index))
new_index = match(ff$value,edge_normal)
table(is.na(new_index))
#isin = match(ff$value,edge_normal)
write.table(ff[c(2,1)],paste(filename,paste(destination,"tcx_node.txt",sep = "/"),sep = "/"),row.names = F,quote = F,col.names = F)
#write.table(ss[c(2,1)],paste(filename,paste(destination,"TCx_node_normal.txt",sep = "/"),sep="/"),row.names = F,quote = F,col.names = F)
write.table(edge_disease,paste(filename,paste(destination,"AD_TCx_92_244.txt",sep = "/"),sep="/"),row.names = F,quote = F,col.names = F)
write.table(edge_normal,paste(filename,paste(destination,"control_TCx_92_217.txt",sep = "/"),sep="/"),row.names = F,quote = F,col.names = F)



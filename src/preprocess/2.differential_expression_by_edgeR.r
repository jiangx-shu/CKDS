library(edgeR)
dictionary = "/Users/jiaminsun/expsjm/single cell/neuron3/aNSC_NPC"
setwd(dictionary)
data = read.table("expression_count_aNSC_NPC.txt")

GBMp = grep("aNSC",colnames(data))
GBMe = grep("NPC",colnames(data))
group = c(rep("aNSC",length(GBMp)),rep("NPC",length(GBMe)))
#构建DGEList对象
dge <- DGEList(
    counts = data, 
    norm.factors = rep(1, length(data[1,])), 
    group = group
)
group_edgeR <- factor(group)
#构建分组
design <- model.matrix(~ group_edgeR)
dge <- estimateDisp(dge, design = design, trend.method = "none")
fit <- glmFit(dge, design)
res <- glmLRT(fit)
write.table(res$table,"DE_by_edgeR_aNSC_NPC.txt",sep = "\t")

#write CPM expression
lib_size = colSums(data)
norm <- t(t(data)/lib_size * median(lib_size)) 
norm = log2(norm+1)
write.table(norm,"expression_CPM_aNSC_NPC.txt")

#select group expression
ast_data = norm[,GBMp]
nsc_data = norm[,GBMe]
write.table(ast_data,"expression_CPM_aNSC.txt")
write.table(nsc_data,"expression_CPM_NPC.txt")

difgene = read.table("DE_by_edgeR_aNSC_NPC.txt")
View(difgene)
difgene$q = p.adjust(difgene$PValue, method = 'fdr')
#differentialgene<- subset(difgene, abs(logFC) > 3.1 & PValue < 0.009 & q<0.05)
differentialgene<- subset(difgene, abs(logFC) > 1 & PValue < 0.05)
dgene=rownames(differentialgene)
View(dgene)
write.table(dgene,"dif_aNSC_NPCgene.txt",row.names = F,col.names = F,quote = F)

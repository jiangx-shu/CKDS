source("http://Bioconductor.org/biocLite.R")
#biocLite("GSEABase")
library(ggplot2)
library(Cairo)
library(DOSE)
library(GO.db)
library(org.Hs.eg.db)
library(org.Mm.eg.db)
library(topGO)
library(GSEABase)
library(clusterProfiler)

########## 2020.01.29
dictionary="/Users/jiaminsun/expsjm/bio/data/GBM_three_groups/GBM/result"
setwd(dictionary)
#????????????
gene_KDS = read.table("analysis_minus_node.txt",header = T)
#二选一
#genetrans_KDS = bitr(gene_KDS$Entrez,fromType = "SYMBOL",toType = "ENTREZID",OrgDb = "org.Hs.eg.db")
genetrans_KDS = bitr(gene_KDS$Entrez,fromType = "SYMBOL",toType = "ENTREZID",OrgDb = "org.Mm.eg.db")
genesKDS = c(genetrans_KDS$ENTREZID)
moduleKDS = c(rep("GBM",nrow(genetrans_KDS)))
dataKDS = data.frame(moduleKDS,genesKDS)
goresultKDS = compareCluster(genesKDS~moduleKDS,
                             data = dataKDS,
                             fun = "enrichGO",
                             readable = T,
                             OrgDb = org.Mm.eg.db)

keggresultKDS = compareCluster(genesKDS~moduleKDS,
                               data = dataKDS,
                               fun = "enrichKEGG",
                               organism = 'mmu')
#organism='hsa')
as.data.frame(keggresultKDS)
dotplot(keggresultKDS)
write.csv(goresultKDS@compareClusterResult,"go_Ast.csv")
write.csv(keggresultKDS@compareClusterResult,"kegg-Ast.csv")
goresultKDS@compareClusterResult$p.adjust = (goresultKDS@compareClusterResult$p.adjust)

p = dotplot(goresultKDS,showCategory=40)
#ggThemeAssistGadget(p)
pdf("result.pdf",width = 15 ,height = 10)
p + aes(color = pvalue) + aes(size = Count)
########## 2020.01.29

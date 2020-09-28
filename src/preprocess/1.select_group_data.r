source("http://bioconductor.org/biocLite.R")
biocLite("org.Hs.eg.db")
biocLite("pandaR")
install.packages("VIM")
library(edgeR)
library(scde)
library(clusterProfiler)
library(org.Hs.eg.db)
dictionary = "/Users/jiaminsun/expsjm/single cell/GBM/GBM2"
setwd(dictionary)
#GBM和FHCN的原始数据
GBMcells=read.csv("GSE84465_GBM.csv",header = T)
Fetalcells=read.table("n_output.txt",header = T)
GBMsymbols=GBMcells$Symbol
Fetalsymbols=Fetalcells$Symbol
symbols=intersect(GBMsymbols,Fetalsymbols)
GBMs=GBMcells[GBMsymbols%in%symbols,]
Fetals=Fetalcells[Fetalsymbols%in%symbols,]
Fetals<-Fetals[,-1]
View(Fetals)
allcounts_allcells=cbind(GBMs,Fetals)
write.table(allcounts_allcells,"countall2.txt",row.names =FALSE)
allcounts_allcells = read.csv("countall2.csv",header=T)
which(duplicated(allcounts_allcells[,1]))
allcounts_allcells=allcounts_allcells[!duplicated(allcounts_allcells$Symbol),]
#start
genename=allcounts_allcells[1,]
genename=allcounts_allcells[row]
gene.df <- bitr(genename, fromType = "ENSEMBL", 
                toType = c("SYMBOL"),
                OrgDb = org.Hs.eg.db)
table(duplicated(gene.df$ENSEMBL))
gene.df = gene.df[!(duplicated(gene.df$ENSEMBL)|duplicated(gene.df$SYMBOL)),]
dim(gene.df)
#分组完成
new_data = allcounts_allcells[rownames(allcounts_allcells)%in%gene.df$ENSEMBL,]
table(rownames(new_data)==gene.df$ENSEMBL)
rownames(new_data) = gene.df$SYMBOL
rownames(new_data)= allcounts_allcells[1,]
rownames(new_data)=allcounts_allcells$Symbol
#end

#allcounts_allcells = read.table("AllCounts_specPops_read_gene_ERCC_filt_FINAL.txt",sep = " ")
#allcounts_allcells = read.csv("counts.csv",row.names = 1)
#oligos<-as.vector(read.table("STAR_oligos_updated_09232015.txt")[,1])
#allcounts_allcells_nooligo<-allcounts_allcells[,-na.omit(match(oligos,colnames(allcounts_allcells)))]
#new GSE76184
new_data=allcounts_allcells
rownames(new_data)= allcounts_allcells$Symbol
allcounts_allcells_nooligo = new_data

#select group
GBMgene=grep("GBM.",colnames(new_data))
Fetalgene=grep("Fetal.",colnames(new_data))
#GBM and FHCN 
select_datape = allcounts_allcells_nooligo[,c(GBMgene,Fetalgene)]



#gene filter
#Filtering for expressed by 5 cells at 10 counts
greaterthan0<-select_datape>2
greaterthan0sum<-rowSums(greaterthan0)
allcounts_comb_genefilt<-select_datape[greaterthan0sum>=5,]
dim(allcounts_comb_genefilt)


#fiiltering for each group by 2 cells at 4 counts
GBMp = grep("GBM.",colnames(allcounts_comb_genefilt))
GBMe = grep("Fetal.",colnames(allcounts_comb_genefilt))
greaterthangroup = allcounts_comb_genefilt[,GBMp]>2
sumgroup = rowSums(greaterthangroup)
allcounts_comb_genefilt =  allcounts_comb_genefilt[sumgroup>=2,] 
greaterthangroup = allcounts_comb_genefilt[,GBMe]>2
sumgroup = rowSums(greaterthangroup)
allcounts_comb_genefilt =  allcounts_comb_genefilt[sumgroup>=2,] 
dim(allcounts_comb_genefilt)
write.table(allcounts_comb_genefilt,"expression_count_GBM.txt")

 
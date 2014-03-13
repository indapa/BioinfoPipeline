library("ggplot2")
library("reshape2")
setwd(getwd())


files <- dir(getwd(), pattern = "*.csv", full.names = FALSE)

for (i in 1:length(files)) {
      #x=read.table(filename,sep=",")
      x=read.table(files[i],sep=",")
          mydata=melt(x)$value
          mydata=t(matrix(mydata,ncol=4, byrow=T))
          colnames(mydata) <-c("AA", "AB", "BB","no.call")
          rownames(mydata) <-c("AA", "AB", "BB", "no.call")

          data.melt=melt(mydata)

          names(data.melt)<-c("pgmsnp", "truth", "value")
          fields <- unlist(strsplit(files[i],"[.]"))
          myfields <- c(fields[1],fields[6],"10x",fields[11])
          myfields
          mytitle=paste(myfields,collapse='.')

          plotname <- paste(mytitle, "png", sep=".")
          p <- ggfluctuation(data.melt) + geom_text(aes(label=data.melt$value)) +xlab("Illumina") + ylab("Pgmsnp") + theme(axis.text.x= element_text(size=rel(1.5))) + theme(axis.text.y= element_text(size=rel(1.5))) + theme(axis.title.x = element_text(size = rel(1.5))) + theme(axis.title.y= element_text(size = rel(1.5))) +  opts(title = mytitle) + theme(plot.title = element_text(size = rel(.95)))
          ggsave(p, file=plotname)



    }

######################################################
## Part II:                                         ##
## Reading in files to do some exploratory analyses ##
######################################################

library(readxl)
library(openxlsx)
library(plyr)
library(XML)
library(RCurl)
library(tidyverse)
library(data.table)
library(RTidyHTML)
doc.raw <- getURL(u)
doc <- tidyHTML(doc.raw)
html <- htmlTreeParse(doc, useInternal = TRUE)
txt <- xpathApply(html, "//body//text()[not(ancestor::script)][not(ancestor::style)][not(ancestor::noscript)]", xmlValue)
cat(unlist(txt))

dir_project <- "/Users/lisa/machine-learning-for-python/webscraping project/"
dir_rawdat <- paste0(dir_project, "raw data/")

files_rawdat <- list.files(dir_rawdat)
files_rawdat <- files_rawdat[!grepl("~", files_rawdat)]

#take all URL.txt
urls <- t(fread(paste0(dir_project, "url.csv"), header = F))
urllink <- gsub("]","",urls[15,])
urllink <- gsub("'","",urllink)

#Collecting all tags
tags <- c()
for (i in files_rawdat){
  print(i)
  tags <- c(tags,excel_sheets(paste0(dir_rawdat,i)))
}

df_tags <- data.frame(tags)
df_tags <- df_tags %>% group_by(tags) %>% dplyr::summarise(n=n())
plot(df_tags)

# There's a lot of tags that are only used in a very few handful of websites. Let's take a look at what kind of tags they are

## Tags that only have one instance
df_tags[df_tags$n == 1,]

## Tags that only have two instances
df_tags[df_tags$n == 2,]

# Look at the most common tags
df_tags <- df_tags[df_tags$n >= round(length(files_rawdat)/2),]
plot(df_tags)

df_tags[order(df_tags$n, decreasing = T),]$tags
# [1] body      full_html h1        head      html      title     a         div       h2        h3        h4        img      
# [13] li        link      meta      p         script    ul        span      footer    i         nav       noscript  section  
# [25] strong   

## It seems like these tags are very typical. May be especially interested in 
## title and meta tags since it contributes more than any other ones for SEO
## Body is not very useful since it's usually a parent node of everything else.

# Let's take a look at the first tab on a random page where it's the full html
test_dat1 <- read.xlsx(paste0(dir_rawdat,files_rawdat[1]), sheet = "full_html", colNames = F)
test_dat1 <- htmlTreeParse(test_dat1[1,1])
test_dat1

# # Want to remove repetitive tags. I want to remove the parent tags and keep all children tags.
# test_tag <- unique(tags)

# Let's look at meta tags
dat_meta_res <- data.frame("name"=c(), "value"=c(), "content"=c())
dat_meta <- read.xlsx(paste0(dir_rawdat, files_rawdat[1]), sheet = "meta")
for(i in 1:nrow(dat_meta)){
  test_dat <- htmlParse(dat_meta[i,], useInternalNodes=T)
  value <- unlist(test_dat['//meta/@value'])
  name <- unlist(test_dat['//meta/@name'])
  content <- unlist(test_dat['//meta/@content'])
  if(is.null(value)){
    value <- NA
  }
  if(is.null(name)){
    name <- NA
  }
  if(is.null(content)){
    content <- NA
  }
  dat_meta <- rbind(dat_meta, data.frame(name, value, content))
}

for (i in 1:nrow(test_dat)){
  test_dat[i,]<- gsub ("\n"," ",test_dat[i,])
  test_line <- htmlParse(test_dat[i,], encoding = "UTF-8")
  getChildrenStrings(xmlRoot(test_line))
}
test_dat 


doc = xmlParse("<doc><a>a string</a> some text <b>another</b></doc>")
getChildrenStrings(xmlRoot(doc))
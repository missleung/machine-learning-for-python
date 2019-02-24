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

# Just realized that no one really webscrapes on multiple pages and try to analyze them at once because
# all pages are set up differently. Hence let's look at the meta tags and title tags that are usually
# set for SEO purposes.

# Let's look at meta tags for SEO purposes. Will use all excel files that are available
data_meta_res_full <- list()

for (j in 1:length(files_rawdat)){
  if("meta" %in% excel_sheets(paste0(dir_rawdat, files_rawdat[j]))){
    print(paste0("Grabbing meta tags from ", files_rawdat[j]))
    dat_meta_res <- data.frame("name"=c(), "value"=c(), "content"=c(), "http_equiv" =c())
    dat_meta <- read.xlsx(paste0(dir_rawdat, files_rawdat[j]), sheet = "meta")
    for(i in 1:nrow(dat_meta)){
      test_dat <- htmlParse(dat_meta[i,], useInternalNodes=T)
      http_equiv <- unlist(test_dat['//meta/@http-equiv'])
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
      if(is.null(http_equiv)){
        http_equiv <- NA
      }
      dat_meta_res <- rbind(dat_meta_res, data.frame(name, value, content, http_equiv))
    }
    data_meta_res_full[[j]] <- dat_meta_res
    names(data_meta_res_full)[j] <- files_rawdat[j]
  }else{
    print(paste0("No meta tags in ", files_rawdat[j]))
  }
}
# [1] "Grabbing meta tags from blog.hubspot.com.xlsx"
# [1] "Grabbing meta tags from blog.wishpond.com.xlsx"
# [1] "Grabbing meta tags from en.wikipedia.org.xlsx"
# [1] "Grabbing meta tags from instapage.com.xlsx"
# [1] "Grabbing meta tags from landerapp.com.xlsx"
# [1] "Grabbing meta tags from mailchimp.com.xlsx"
# [1] "No meta tags in neilpatel.com.xlsx"
# [1] "No meta tags in thelandingpagecourse.com.xlsx"
# [1] "No meta tags in unbounce.com.xlsx"
# [1] "Grabbing meta tags from www.crazyegg.com.xlsx"
# [1] "Grabbing meta tags from www.simplemarketingnow.com.xlsx"

# Taking a look at a couple of websites

data_meta_res_full$blog.hubspot.com.xlsx$name # This website seems to also focus heavily on twitter
data_meta_res_full$blog.hubspot.com.xlsx$value
data_meta_res_full$blog.hubspot.com.xlsx$content 
# Interesting...there's a few duplicates on the content and only a handful of lines that could be useful to understand the key words

data_meta_res_full$instapage.com.xlsx$name
data_meta_res_full$instapage.com.xlsx$value
data_meta_res_full$instapage.com.xlsx$content 
data_meta_res_full$instapage.com.xlsx$http_equiv

data_meta_res_full$www.crazyegg.com.xlsx$name
data_meta_res_full$www.crazyegg.com.xlsx$value
data_meta_res_full$www.crazyegg.com.xlsx$content
data_meta_res_full$www.crazyegg.com.xlsx$http_equiv

doc = xmlParse("<doc><a>a string</a> some text <b>another</b></doc>")
getChildrenStrings(xmlRoot(doc))